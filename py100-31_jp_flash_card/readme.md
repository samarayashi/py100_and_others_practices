## 使用說明  
1. 以利用pyinstaller打包，可直接執行  
2. 單字集統一放在words_resource中，預設抓有n1~n5的單字，也可放入自己命名的單字集  
3. 將已經會的單字剃除，自動產生XX_to_learn的檔案放入剩餘單字，下次會優先讀取XX_to_learn  
4. 當日所不會的單字會在learning_record中留下紀錄可供複習  

## 技術項目  
1. os.path使用  
2. csv檔案應用與處理  
3. tkinter應用  
4. pyinstaller打包  
  `pip install pyinstaller`  
  `python -m PyInstaller -D -w --icon=shrine.ico main.py`  
  	-D 以資料夾輸出  
    	-w 取消console  
    	--icon 更換icon  
  打包備註：  
    - 若留有console，在cmd中開啟exe檔可停留在console上可以查看報錯內容。直接點擊的話，報錯即消失 => 閃退  
    - windows留有icon cache，測試時同路徑下多次打包後的icon可能會不正常顯示 => 更換路徑或手動清除暫存即可正常顯示  
    - 將被引用的靜態資料夾丟入編譯完的路徑中，讓編譯完後的程式可以抓取  
