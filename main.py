import json
from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.factory import Factory
# factory is to get instance of dynamic class (i.e. class cerated without declaration)
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty

token = "bb233f234bc3eb3df4ecb30859da8d9e"
class AddLocationForm(BoxLayout):
    search_input = ObjectProperty()
    search_results = ObjectProperty()

    def search_location(self):
        search_template = "http://api.openweathermap.org/data/2.5/" + \
                          "find?q={}&type=like&APPID=" + token
        search_url = search_template.format(self.search_input.text)
        request = UrlRequest(search_url, self.found_location)

    """
    found location will be triggered after getting response from url request.
    """
    def found_location(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        if data and 'list' in data:
            cities = [(d['name'], d['sys']['country']) for d in data['list']]
            # cities = ["{} ({})".format(d['name'], d['sys']['country'])
            #           for d in data['list']]
            self.search_results.item_strings = cities
            del self.search_results.adapter.data[:]
            # self.search_results.adapter.data.clear() #introduced in python3
            self.search_results.adapter.data.extend(cities)
            self.search_results._trigger_reset_populate()
        else:
            del self.search_results.adapter.data[:]
            # self.search_results.adapter.data.clear() #introduced in python3
            self.search_results._trigger_reset_populate()

        """ custom function called args_converter.This function should accept two values: the index of the item being rendered,
        and the item itself.Kivy will call this function repeatedly for each item in the underlying data list
        NEED to set arg converter for adapter in kv file"""
    def args_converter(self, index, data_item):
        city, country = data_item
        return {'location': (city, country)}

class LocationButton(ListItemButton):
    location = ListProperty()


class CurrentWeather(BoxLayout):
    location = ListProperty(['New York', 'US'])
    conditions = StringProperty()
    temp = NumericProperty()
    temp_min = NumericProperty()
    temp_max = NumericProperty()

    def update_weather(self):
        weather_template = "http://api.openweathermap.org/data/2.5/" +\
                           "weather?q={},{}&units=metric&APPID=" + token
        weather_url = weather_template.format(*self.location)
        request = UrlRequest(weather_url, self.weather_retrieved)

    def weather_retrieved(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        self.conditions = data['weather'][0]['description']
        self.temp = data['main']['temp']
        self.temp_min = data['main']['temp_min']
        self.temp_max = data['main']['temp_max']

class WeatherRoot(BoxLayout):
    addlocation = ObjectProperty()
    current_weather = ObjectProperty()

    def show_current_weather(self, location=None):
        self.clear_widgets()
        if self.current_weather is None:
            self.current_weather = CurrentWeather()
        if location is not None:
            self.current_weather.location = location
        self.current_weather.update_weather()
        self.add_widget(self.current_weather)

    def show_add_location_form(self):
        self.clear_widgets()
        self.add_widget(self.addlocation)

class WeatherApp(App):
    pass

if __name__ == '__main__':
    WeatherApp().run()