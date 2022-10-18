<h1 align="center"> COVID-19 Hospital Bed Management System </h1>
<h2 align="center"> An application which provides real-time statistics for COVID-19 bed availability status</h2>

[![Project Status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

## Table of Contents
* **[Motivation](#motivation)**
* **[Real-time bed availability status](#real-time-bed-availability-status)**
* **[Gallery](#gallery)**
* **[Tech Stack](#tech-stack)**
* **[Functionalities](#functionalities)**
* **[To Do and Further Improvements](#to-do-and-further-improvements)**
* **[Requirements](#requirements)**
* **[Run Locally](#run-locally)**
* **[License](#license)**
* **[Contributors](#contributors)**

## Motivation
During the COVID-19 pandemic, finding beds in hospitals was an uphill task and in order to
assist patients in finding beds easily this app has been developed. The app allows users to 
easily view the current bed availability status (as provided by BBMP) and also previous
trends for a given hospital/COVID Care Centre

## Real-time bed availability status
The crux of this solution lies in collecting real-time bed availability status from BBMP. BBMP have currently stopped updating the statistics on their website, post the pandemic

## Gallery

### Home Page
![Home Page](https://raw.githubusercontent.com/prabhav5112/CHBMS-app/main/media/Home.png)
### About
![About](https://raw.githubusercontent.com/prabhav5112/CHBMS-app/main/media/About.png)
### Brief overview for a class of hospitals
![Brief overview for a class of hospitals](https://raw.githubusercontent.com/prabhav5112/CHBMS-app/main/media/Hospital_overview.png)
### Detailed statistics for a hospital
![Detailed statistics for a hospital](https://raw.githubusercontent.com/prabhav5112/CHBMS-app/main/media/Hospital_detailed.png)
### Login history
![Login history](https://raw.githubusercontent.com/prabhav5112/CHBMS-app/main/media/Login_history.png)
### Light theme
![Light theme](https://raw.githubusercontent.com/prabhav5112/CHBMS-app/main/media/Light_theme.png)

## Tech Stack
* Tkinter has been used for the front-end
* MySQL has been used as a back-end database server
* The application has been developed using Python


## Functionalities
* Show real-time statistics for bed status in various hospitals
* Show various illustrative graphs
* Allow administrators to change the bed availbaility statuses


## To Do and Further Improvements
- [x] Using matplotlib, seaborn to plot trends for various hospitals
- [x] Develop an app with light and dark themes
- [x] Allow administrators to update the bed availability status
- [ ] Show trends for hospitals upto the date available in the database
- [ ] Updating the size of the hospital overview graphs

## Requirements
The following dependencies and modules (python) are required, to run this locally 
* SQLAlchemy==1.4.41
* pyplot-themes==0.2.2
* matplotlib==3.5.3
* pillow==9.2.0
* pandas==1.5.0
* lxml==4.9.1
* progressbar==2.5
* seaborn==0.12.1
* tk==0.1.0

## Run Locally
- **Clone the GitHub repository**
```python
$ git clone git@github.com:prabhav5112/CHBMS-app.git
```

- **Move to the Project Directory**
```python
$ cd CHBMS-app
```

- **Create a Virtual Environment (Optional)**

   * Install Virtualenv using pip (If it is not installed)
   ```python
    $ pip install virtualenv
    ```
   * Create the Virtual Environment
   ```python
   $ virtualenv chbms
   ```
   * Activate the Virtual Environment 
   
      * In MAC OS/Linux 
      ```python
      $ source chbms/bin/activate
      ```
      * In Windows
      ```python
      $ source chbms\Scripts\activate
      ```
  
- **Install the [requirements](requirements.txt)**
```python
(chbms) $ pip install -r requirements.txt
```

- **Load the database from the MySQL file**
```python
(chbms) $ mysql project < Project_db_Nov_27.sql -p
```

- **Run the python script [main.py](main.py)**
```python
(chbms) $ python3 main.py
```


- **Dectivate the Virtual Environment (after you are done)**
```python
(chbms) $ deactivate
```

## License 
[![License](https://img.shields.io/badge/License-Apache%202.0-red.svg)](https://opensource.org/licenses/Apache-2.0)
<br/>
This project is under the Apache-2.0 License License. See [LICENSE](LICENSE) for Details.

## Contributors
<table>
  <tr>
    <td align="center"><img src="https://avatars.githubusercontent.com/u/91932766?s=400&v=4" width="100px;" height="100px;" alt=""/><br/><sub><b>Prabhav B Kashyap</b></sub></a><br/><p align="center">
      <p align="center">
        <a href="https://www.linkedin.com/in/prabhav-b-kashyap/" alt="Linkedin">
          <img src="http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width = "30">
        </a>
        <a href="https://github.com/prabhav5112" alt="Github">
          <img src="http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width = "30">
        </a>
      </p>
    </td>
  </tr>
</table>
