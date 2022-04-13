1. restful-api簡述  
    - 網頁的api基於http協定，api發送的形式要是http能理解的樣子。
    - 也有其他協定，如ftp就是基於檔案傳輸的協定，亦有其規則。
    - restful-api是一種符合http動詞url設計風格，讓url的可讀性和其背後運作的http動詞(request method)一致。
  
2. 常用http動詞  
	- get: read data  
		  /random, /all, /search
	- post: create data  
		  /add
	- put: update entire data  
	- patch: update part of data  
		  /update-price/<int:cafe_id>  
	- delete: delete data  
		  /report-closed/<int:cafe_id>

3. 可利用postman產生api-document  
    - 利用postman或是curl(cmd), requests(python)模組：才能執行不同動作的request method(get, post, put, patch, put, delete)去打相關api  
    - 瀏覽器中輸入url默認都是get, 而網頁表單提交的動作默認為post  

4. 網頁表單只有post方法  
    - 所以在網頁中即使是update的動作，仍然使用post，而非put/patch
