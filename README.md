透過官方帳號進行推播會因為人數越來越多而增加發送成本，因此 Line Notify是一個官方提供帳號來傳送通知，重要的是免費!!

首先登入到 <a href='https://notify-bot.line.me/zh_TW/'>LINE Notify</a> 並進入到個人頁面
<img src='https://blogger.googleusercontent.com/img/a/AVvXsEjGtEyo3KApyUqKIb1JMb1XDv-XnyS8MHuy_l9Ptpb8ECcN5cZyOj0_U_g9anajMuUfWjcYdG570bULM3ddXVR8mgM61co4U_ST0k3jWq8kB1DU-pQxGCLMUKKT5fsDuTeI1XxsxMtPV2RdZVTNpbBwjEK3fUaVmCAj4PudsmlCbqjeY1izva4053IR=w640-h380'>

選擇要接收通知的聊天室
<img src='https://blogger.googleusercontent.com/img/a/AVvXsEguvEEzZ_HxCxa8clBUk2ifA-Bp3A-bIgUnhvTk4CthzzcxnQ7_HYxsOVEIuXyccJYgJh23XYVyNMcZCbA5xqisisFy8zHAw7NFgQ4WQ_J09spjMggEQ2yCoCQfdD7R5U4aoT2rjJixxPkEG2MzWacl2yFZDr6V5bmhyMW_XtiEUkC3tqSvdDF4XXbJ=w640-h494'>

把產生的權證記錄下來，如果遺失或忘記的話就只能重新連接獲取新的權證
<img src='https://blogger.googleusercontent.com/img/a/AVvXsEiTxi4CliZrN_fqiNhGpZWOB7uJ-8nEpJWcRBNC9E2tf_KgIAOvPchmdw78ylTzTmaWcgqLgiXCz4PhSHb2tAzc2XLdPmoKA1-S-ggu5gSXkyPA9o1VTf604i_EuikfZAAogaWe6Z6oXUWaxiSuSiN92VRhLKTFcbHGIBv23_KBXaks0aL40yiAjyiB=w640-h366'>

這樣到這邊 Line Notify 的設定就完成了，接著看程式碼。

使用到的 python 模組
<ul>
    <li>requests：建立與 Dcard 之間連線，獲取我們要的網頁資料</li>
    <li>bs4：BeautifulSoup是一個用來解析HTML結構的Python套件</li>
    <li>re：利用正則表達式分析url</li>
    <li>time：用 time.sleep() 進行睡眠，降低發送 request 頻率</li>
    <li>datetime：取得當前時間</li>
    <li>sqlite3：簡單紀錄文章資訊</li>
</ul>


lineNotifyMessage() 參數設定
<ul>
    <li>token：傳送權證</li>
    <li>message：傳送要發送的訊息</li>
    <li>img：傳送要發送的圖片url</li>
    <li>isNotificationDisabled ：是否要收到通知</li>
</ul>
