/*
Copyright © 2020 NAME HERE <EMAIL ADDRESS>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
package cmd

import (
	f "github.com/Mr-Linus/fast-pull/pkg/file"
	"github.com/Mr-Linus/fast-pull/pkg/images"
	"github.com/Mr-Linus/fast-pull/pkg/log"
	"github.com/spf13/cobra"
)

// getCmd represents the get command
var (
	getCmd = &cobra.Command{
		Use:   "get",
		Short: "Pull Your image",
		Long: `Pull Your image`,
		Run: func(cmd *cobra.Command, args []string) {
			if file == ""{
				if image == ""{
					log.Print("Images are not set.")
				}
				if err := images.SyncImage(image); err != nil {
					log.ErrPrint(err)
				}
				return
			}
			imgs := f.ReadImage(file)
			if imgs == nil{
				log.Print("Images are not set.")
				return
			}
			for _,img := range imgs{
				if err := images.SyncImage(img); err != nil {
					log.ErrPrint(err)
				}
			}
			return
		},
	}
	image string
	file string
)
func init() {
	rootCmd.AddCommand(getCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	getCmd.PersistentFlags().StringVarP(&image,"image", "i", "","The image you need to pull")
	getCmd.PersistentFlags().StringVarP(&file,"file", "f", "","The file of the image you need to pull")
	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// getCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
