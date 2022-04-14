Description:
	In the google form, one page records the country you want to go to and the acceptable price , and the other page records the mailbox of the person you want to notify. Use Sheety API to get needed information from google sheet, then use Tequila's API to query flight information. If there is a flight that meets the needs, it will send email or SMS notification.

Technical items:
1. third-party API
    Use Sheety to control google form - https://Sheety.co/
    Use Tequila to get flight information - https://tequila.kiwi.com/portal/docs/tequila_api
	Use TWILIO-SMS to send SMS notification - https://www.twilio.com/docs/sms/api
2. SMTP to send email.
3. Deploy it on PythonAnywhere

Structure:
	Model: 
		flight_data.py: flight information
	Controller: 
		data_manager.py: get destination and poersonal information from google sheet
		flight_search.py: get flight information from Tequila
		notification_manager.py: send mail or SMS
	Entrance:
		main.py
		
		
程式說明：
google表單中，一頁記錄想去的國家與可接受價格，另一頁紀錄欲通知人的信箱。利用Sheety讀取表單資訊後，利用Tequila的API查詢航班資訊，若有符合需求的航班即發信或寄簡訊通知。

技術項目：
1. 操作第三方API
	Sheety操作google表單 - https://Sheety.co/
	Tequila獲得航班資訊 - https://tequila.kiwi.com/portal/docs/tequila_api
	TWILIO-SMS發送簡訊 - https://www.twilio.com/docs/sms/api
2. SMTP寄信
3. PythonAnywhere部署

