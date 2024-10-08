
# Pajer_1.0


**Pajer_1.0** is a Time Attendance System. It allows you to track employee attendance by using an RFID reader and a connected database. The system is adaptable for use on various operating systems with minimal modifications to the code.

![image](https://github.com/SmolinskiP/Pajer_1.0/assets/49648588/3e6ae949-02a2-44e2-b387-84bf9a701654)

![image](https://github.com/SmolinskiP/Pajer_1.0/assets/49648588/ec2d897e-ff28-47b5-88cd-755bf95b0a63)

## Requirements:

- UART USB Converter [LINK](https://www.aliexpress.com/item/1005003292190035.html?spm=a2g0o.productlist.main.5.16b6140d8GOvws&algo_pvid=efb61b3f-855d-4b4d-9d26-4174b9996db1&algo_exp_id=efb61b3f-855d-4b4d-9d26-4174b9996db1-2&pdp_npi=4%40dis%21PLN%2118.02%2110.82%21%21%214.28%21%21%4021038edf16921831215858663e3efc%2112000025051327922%21sea%21PL%210%21A&curPageLogUid=SEjpEf7GxtU5) (just an example, can be any)
- RFID Reader [LINK](https://www.aliexpress.com/item/4000067465590.html?spm=a2g0o.detail.1000060.1.57b81c99zDuN8p&gps-id=pcDetailBottomMoreThisSeller&scm=1007.13339.169870.0&scm_id=1007.13339.169870.0&scm-url=1007.13339.169870.0&pvid=2259797a-f788-425d-ae4e-221e6b91d645&_t=gps-id:pcDetailBottomMoreThisSeller,scm-url:1007.13339.169870.0,pvid:2259797a-f788-425d-ae4e-221e6b91d645,tpp_buckets:668%232846%238108%231977&&pdp_ext_f=%7B%22sku_id%22:%2212000018138193929%22,%22sceneId%22:%223339%22%7D) (just an example, can be any with serial communication)
- Some cables to connect them:

  ![image](https://github.com/SmolinskiP/Pajer_1.0/assets/49648588/f732247e-f309-45a8-a1fb-ebcad9c13951)
- RFID Cards
- Local / Remote Database (tested on MariaDB - [LINK](https://mariadb.org/download/)))
- Copy the RCP folder to the device to which you have connected the reader.
- Change the "port" in `readrs.py`:

```python
ser = serial.Serial(
        port='COM7',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.2,
)
```

- Change connection params in function `Insert_SQL_Remote`:

```python
conn3 = database.connect(
        user="rcp",
        password="STRONGPASSWORD",
        host="XXX.XXX.XXX.XXX",
        database="RFID"
        )
```

## Run with:

- `startbat.vbs`
- `python readrs.py`

There is also a function to turn on the computer for an employee who logs in, but this already requires changes in the database which I will not discuss here. Code was tested on Debian11 / Windows10. To change the system small changes in the code are required, currently the application is adapted to run on Windows.

## Database Setup:

The next step is to create tables in the database. We do this by running the main database application. We do this either by installing it with an `.exe` file in releases or by cloning the repo and running `python Pajer.py`. The first run will ask us whether to create tables and to specify the connection parameters. **NOTE: THE DATABASE ENGINE MUST BE INSTALLED BEFOREHAND!!!** In case of problems, we create the database manually using the `DB.sql` file located in the application's main folder.

When you have done all this, reset the application and log in with:

- **login/password:** `admin / qwerty`
