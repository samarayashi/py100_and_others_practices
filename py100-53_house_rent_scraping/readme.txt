程式說明：
利用selenium爬取租房網站zillow租房資訊，模仿data entry的流程，將爬取資訊填入google表單。

實作細節：
1. header中加入user-agent和accept-language
	建立agent-pool去模擬使用者header
2. 並非靜態網頁，模擬使用者行為觸發網頁內容後再爬取
	selenium中利用ActionChains做出向下滑動的效果
3. 會遇到captcha，但其判斷較為簡單，點擊長壓按鈕即可
	判斷為captcha畫面後，利用ActionChains模擬驗證動作
4. 利用css selector與xpath定位所欲抓取元素

selenium補充：
1. 欲控制瀏覽器畫面內元素有兩種方法
	- driver.execute_script去調用javascript方法
	- 利用ActionChains對webdriver做更多底層且細節的操作

2. selenium是模仿user操作瀏覽器
	- selenium原生的click，若元素不在視域之中會報錯(可以定位，但無法點擊)
	- 盡量將視窗最大化讓元素定位準確
	- ActionChains:action.move_to_element(element)
	- 使用javascript的click
	
3. Can not click on a Element: ElementClickInterceptedException
	....is not clickable at point....other element would receive the click
	普遍解法：	
		- ActionChains：滾動到需要的元素，然後執行點擊
		- execute_script：利用javascript點擊，或是滾動視窗
		- 等待機制；待上層元素消失

4. 打印元素內容debug
	利用outerHTML屬性，element.get_attribute('outerHTML')
	
5. 等待機制
	sleep(強制等待)、Implicit Waits(隱式等待)、Explicit Waits(顯式等待)
	



