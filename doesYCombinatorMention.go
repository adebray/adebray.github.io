/* Detects if Go, the programming language, is mentioned on the front page of Hacker News.
 * A little bit of thought is necessary to ensure words such as 'ago' and 'Google' don't
 * register as false positives. Thus, 'Go' is required to be in uppercase and form its own
 * word in the text. This will cause some false positives, but not many -- in headlines,
 * the first word tends not to be a verb, and references to the board game Go are less
 * common on a programming website than references to the language.
 *
 * Arun Debray, September 5, 2013
 */

package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
)

// This is not beautiful code, but seems like the easiest way to detect word boundaries that
// are likely to be meaningful. Suggestions are welcome...
func isGoOnTheFrontpage(body []byte) bool {
	source := string(body)
	strings.Replace(source, ".", " ", -1)
	strings.Replace(source, ",", " ", -1)
	strings.Replace(source, ":", " ", -1)
	strings.Replace(source, ";", " ", -1)
	strings.Replace(source, "\"", " ", -1)
	return strings.Contains(source, "Go ") ||
		strings.Contains(source, "golang") ||
		strings.Contains(source, "Golang")
}

func main() {
	resp, err := http.Get("https://news.ycombinator.com/")
	if err != nil {
		panic(err.Error())
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		panic(err.Error())
	}
	if isGoOnTheFrontpage(body) {
		fmt.Println("Yes, Go is on the frontpage of Hacker News.")
	} else {
		fmt.Println("No, Go isn't on the frontpage of Hacker News.")
	}
}
