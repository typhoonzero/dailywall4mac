package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"os/exec"
)

type bingJsonResponse struct {
	Images   []map[string]interface{}
	Tooltips map[string]string
}

func downloadBingWallPaper(host, w, h, uhd, outputDir string) (string, error) {
	jsonURL := fmt.Sprintf("https://%s/HPImageArchive.aspx?format=js&idx=0&n=1&uhdwidth=%s&uhdheight=%s&uhd=%s",
		host, w, h, uhd)
	resp, err := http.Get(jsonURL)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}
	resultJson := bingJsonResponse{}
	err = json.Unmarshal(body, &resultJson)
	if err != nil {
		return "", err
	}
	if len(resultJson.Images) < 1 {
		return "", fmt.Errorf("bing json response got no images list: %s\nerr: %s", string(body), err)
	}
	imageURL := resultJson.Images[0]["url"].(string)
	imageFullURL := fmt.Sprintf("https://%s%s", host, imageURL)
	u, err := url.Parse(imageFullURL)
	if err != nil {
		return "", err
	}
	m, _ := url.ParseQuery(u.RawQuery)
	imageFileName := m["id"][0]

	outputFile := outputDir + "/" + imageFileName
	if _, err := os.Stat(outputFile); err == nil {
		fmt.Printf("skip downloading %s\n", outputFile)
		return outputFile, nil
	}

	imageResp, err := http.Get(imageFullURL)
	if err != nil {
		return "", err
	}
	if imageResp.StatusCode != 200 {
		return "", fmt.Errorf("image url returned non 200 code: %s", imageFullURL)
	}
	defer imageResp.Body.Close()
	f, err := os.Create(outputFile)
	if err != nil {
		return "", err
	}
	defer f.Close()
	_, err = io.Copy(f, imageResp.Body)
	if err != nil {
		return "", err
	}
	return outputFile, nil
}

var setWallPaperMultiScreen = `/usr/bin/osascript<<END
tell application "System Events"
    set desktopCount to count of desktops
    repeat with desktopNumber from 1 to desktopCount
        tell desktop desktopNumber
            set picture to "%s"
        end tell
    end repeat
end tell
END
`

func main() {
	defaultHost := "www.bing.com"
	defaultW := "3840"
	defaultH := "2160"
	defaultUHD := "1"
	homedir, err := os.UserHomeDir()
	if err != nil {
		panic(err)
	}
	defaultOutputDir := homedir + "/bing-wallpapers"
	host := os.Getenv("BING_WALLPAPER_HOST")
	width := os.Getenv("BING_WALLPAPER_WIDTH")
	height := os.Getenv("BING_WALLPAPER_HEIGHT")
	uhd := os.Getenv("BING_WALLPAPER_UHD")
	outputDir := os.Getenv("BING_WALLPAPER_OUTPUT_DIR")

	if host == "" {
		host = defaultHost
	}
	if width == "" {
		width = defaultW
	}
	if height == "" {
		height = defaultH
	}
	if uhd == "" {
		uhd = defaultUHD
	}
	if outputDir == "" {
		outputDir = defaultOutputDir
	}
	os.MkdirAll(outputDir, 0755)

	downloadedImage, err := downloadBingWallPaper(host, width, height, uhd, outputDir)
	if err != nil {
		panic(err)
	}
	cmdLines := fmt.Sprintf(setWallPaperMultiScreen, downloadedImage)
	cmd := exec.Command("/bin/sh", "-c", cmdLines)
	err = cmd.Run()
	if err != nil {
		panic(err)
	}
}
