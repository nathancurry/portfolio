import requests
from datetime import datetime, timedelta
import os
from time import sleep
from config import LAT, LON



class SunriseSunset():
    def __init__(self, lat:float = LAT, lon:float = LON, interval_hours:int = 24):
        self.latitude = lat
        self.longitude = lon

        self.api_endpoint = "https://api.sunrise-sunset.org/json"
        self.api_parameters = {'lat': self.latitude, 'lng': self.longitude, 'formatted': 0}
        self.api_date_format = '%Y-%m-%dT%H:%M:%S+00:00'
        
        self.update_interval_hours = interval_hours
        self.data: dict = None
        self.sunrise: datetime.time = None
        self.sunset: datetime.time = None
        self.last_update: datetime = None
        self.query_api()
    
    def get_sunrise(self, format_string:str = None):
        self.refresh_data()
        if self.last_update + timedelta(hours=12) > datetime.now():
            self.query_api()
        if not format_string:
            return self.sunrise.strftime(format_string)
        else:
            return self.sunrise

    def get_sunset(self, format_string:str = None):
        self.refresh_data()
        if format_string:
            return self.sunset.strftime(format_string)
        else:
            return self.sunset

    def is_day(self) -> bool:
        self.refresh_data()
        now = datetime.now()
        if now.time() < self.sunrise or now.time() > self.sunset:
            return False
        else:
            return True

    def refresh_data(self):
        if self.last_update + timedelta(hours=self.update_interval_hours) > datetime.now():
            self.query_api()

    def query_api(self):
        response = requests.get(self.api_endpoint, params=self.api_parameters)
        response.raise_for_status()
        self.data = response.json()
        self.sunrise = datetime.strptime(self.data['results']['sunrise'], self.api_date_format).time()
        self.sunset = datetime.strptime(self.data['results']['sunset'], self.api_date_format).time()
        self.last_update = datetime.now()


class ISSPosition():
    def __init__(self, lat:float = LAT, lon:float = LON):
        self.latitude = lat
        self.longitude = lon

        self.iss_latitude: float = None
        self.iss_longitude: float = None

        self.api_endpoint = "http://api.open-notify.org/iss-now.json"
        self.data: dict = None
        self.query_api()

    def is_overhead(self) -> bool:
        if abs(self.latitude - self.iss_latitude) > 5:
            return False
        if abs(self.longitude - self.iss_longitude) > 5:
            return False
        return True

    def query_api(self) -> None:
        response = requests.get(self.api_endpoint)
        response.raise_for_status()
        self.data = response.json()
        self.iss_latitude = float(self.data["iss_position"]["latitude"])
        self.iss_longitude = float(self.data["iss_position"]["longitude"])


class ISSNotifier():
    def __init__(self, sun:SunriseSunset, iss:ISSPosition, interval_minutes:int = 5, notify_type = "desktop"):
        self.sunrise_sunset = sun
        self.iss_position = iss
        self.title: str = "ISS Notifier"
        self.message: str = "The ISS is visible!"

        self._valid_types = ['mac_popup', 'win_popup', 'email']
        self._default_type = 'mac_popup'
        self.notify_type = notify_type
    
    @property
    def notify_type(self):
        return self._notify_type
    
    @notify_type.setter
    def notify_type(self, value):
        if value in self._valid_types:
            self._notify_type = value
        else:
            self._notify_type = self._default_type


    def is_visible(self) -> bool:
        if self.sunrise_sunset.is_day():
            return False
        if not self.iss_position.is_overhead():
            return False
        else:
            return True

    def notify(self):
        if not self.is_visible():
            print("Can't see the ISS")
            return
        self.send_notification()

    def send_notification(self):
        if not self.message or not self.title:
            self.message = "Configure ISS Notifier"
            self.title = "Configure ISS Notifier"
        if self.notify_type == 'mac_popup':
            self.send_mac_popup()
        elif self.notify_type == 'win_popup':
            self.send_win_popup()
        elif self.notify_type == 'email':
            self.send_email()
        else:
            raise Exception


    def send_mac_popup(self):
        ok = '{"OK"}'
        time = datetime.now().strftime("%d %B, %Y, %H:%M:%S")
        command = f'display dialog "{time}: {self.message}" with title "{self.title}" buttons {ok} default button "OK"'
        os.system(f"osascript -e '{command}'")

    def send_win_popup(self):
        pass

    def send_email(self):
        pass

        
def main():
    sun = SunriseSunset()
    iss = ISSPosition()
    notifier = ISSNotifier(sun, iss)

    while True:
        notifier.notify()
        sleep(10)

if __name__ == '__main__':
    main()