package main

import (
	"encoding/json"
	"io/ioutil"
	"net/http"
	"os"

	"./checker"
	"github.com/gin-gonic/gin"
)

func main() {

	router := gin.Default()
	gin.SetMode(gin.ReleaseMode)
	router.GET("/", func(c *gin.Context) {
		c.String(http.StatusOK, "Hello? \nWho's there? \nPlz log in before any words")
	})

	v1Group := router.Group("/v1", func(c *gin.Context) {
	})
	{
		v1Group.GET("/login", func(c *gin.Context) {
			name := c.DefaultQuery("name", "Guest")

			var slice []map[string]interface{}
			var m2 map[string]interface{}
			m2 = make(map[string]interface{})
			m2["name"] = name
			slice = append(slice, m2)

			data, err := json.Marshal(slice)
			if err == nil {
				ioutil.WriteFile("./config", data, 0644)
				c.String(http.StatusOK, "Alright! \nNow I got it I got it...")
			}
		})
	}

	v2Group := router.Group("/v2", func(c *gin.Context) {
		_, err := os.Stat("./config")
		if err == nil {
			c.Next()
		}
		c.Abort()
	})
	{
		v2Group.GET("/user", func(c *gin.Context) {
			data := []byte("-1 10 1 10 4 10 5 2 1 20 10 3 11 -2 -1 18 11 -2 -1 2 1 22 8 1 7 6 1 2 1 12 3 -11 1 2 1 13 20 11 -2 -1 29 0 11 -2 -1 10 2 21 8 22 7 5 2 2 20 10 3 1 2 1 8 23 7 9 24 20 10 6 2 1 12 3 -13 11 -2 -1 2 1 26 2 73 20 10 7 2 2 26 2 89 20 10 7 2 3 26 2 70 20 10 7 2 4 26 2 84 20 10 7 2 5 26 2 -111 20 10 7 2 6 26 2 116 20 10 7 2 7 26 2 103 20 10 7 2 8 26 2 124 20 10 7 2 9 26 2 121 20 10 7 2 10 26 2 102 20 10 7 2 11 26 2 99 20 10 7 2 12 26 2 42 20 10 7 2 13 26 2 124 20 10 7 2 14 26 2 77 20 10 7 2 15 26 2 121 20 10 7 2 16 26 2 123 20 10 7 2 17 26 2 43 20 10 7 2 18 26 2 43 20 10 7 2 19 26 2 77 20 10 7 2 20 26 2 43 20 10 7 2 21 26 2 43 20 10 7 2 22 26 2 111 20 10 7 11 -2 -1 21 22 2 122 17 23 11 -2 -1 10 8 27 22 21 13 8 4 7 5 2 2 20 10 3 11 -2 -1 21 2 108 17 20 11 -2 -2 ")
			ioutil.WriteFile("./asdf", data, 0644)
			c.String(http.StatusOK, "Initialization finished!")
		})
		v2Group.GET("/flag", func(c *gin.Context) {
			flag := []byte(c.DefaultQuery("flag", "this is flag"))
			ioutil.WriteFile("./hjkl", flag, 0644)
			c.String(http.StatusOK, "Flag's being read\n")
		})
	}

	v3Group := router.Group("/v3", func(c *gin.Context) {
		_, err := os.Stat("./asdf")
		if err == nil {
			_, err := os.Stat("./hjkl")
			if err == nil {
				c.Next()
			}
		}
		c.Abort()
	})
	{
		v3Group.GET("/check", func(c *gin.Context) {
			var cc int
			cc = checker.Check()
			if cc == 1 {
				c.String(http.StatusOK, "wow!!! Your flag is real! \nnice work! \nGo and submit, come on!")
				c.Next()
			} else {
				c.String(http.StatusOK, "no!!no no! Wait!\nWhy use fake flag???! \nAre you fooling me around\n?_?")
				c.Next()
			}
		})
	}

	router.Run(":8000")
}
