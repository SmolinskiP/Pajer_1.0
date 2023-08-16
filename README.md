# Pajer_1.0

Requirements:
1. UART USB Converter [LINK](https://www.aliexpress.com/item/1005003292190035.html?spm=a2g0o.productlist.main.5.16b6140d8GOvws&algo_pvid=efb61b3f-855d-4b4d-9d26-4174b9996db1&algo_exp_id=efb61b3f-855d-4b4d-9d26-4174b9996db1-2&pdp_npi=4%40dis%21PLN%2118.02%2110.82%21%21%214.28%21%21%4021038edf16921831215858663e3efc%2112000025051327922%21sea%21PL%210%21A&curPageLogUid=SEjpEf7GxtU5) (just an example, can by any)
2. RFID Reader [LINK](https://www.aliexpress.com/item/4000067465590.html?spm=a2g0o.detail.1000060.1.57b81c99zDuN8p&gps-id=pcDetailBottomMoreThisSeller&scm=1007.13339.169870.0&scm_id=1007.13339.169870.0&scm-url=1007.13339.169870.0&pvid=2259797a-f788-425d-ae4e-221e6b91d645&_t=gps-id:pcDetailBottomMoreThisSeller,scm-url:1007.13339.169870.0,pvid:2259797a-f788-425d-ae4e-221e6b91d645,tpp_buckets:668%232846%238108%231977&&pdp_ext_f=%7B%22sku_id%22:%2212000018138193929%22,%22sceneId%22:%223339%22%7D) (just an example, can by any with serial communication)
3. Some cables to connect them:<br />
![image](https://github.com/SmolinskiP/Pajer_1.0/assets/49648588/f732247e-f309-45a8-a1fb-ebcad9c13951)
4. RFID Cards
5. Local / Remote Database (tested on MariaDB - [LINK](https://mariadb.org/download/))


Copy the RCP folder to the device to which you have connected the reader<br />
Change the "port" in:
```
ser = serial.Serial(
        port='COM7',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.2,
)
```
Change connection params in function "Insert_SQL_Remote":
```
conn3 = database.connect(
        user="rcp",
        password="STRONGPASSWORD",
        host="XXX.XXX.XXX.XXX",
        database="RFID"
        )
```
Run with:
1. startbat.vbs
2. ```python readrs.py```
There is also a function to turn on the computer for an employee who logs in, but this already requires changes in the database which I will not discuss here<br />
Code was tested on Debian11 / Windows10. To change the system small changes in the code are required, currently the application is adapted to run on windows.<br />
