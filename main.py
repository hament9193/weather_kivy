import json
from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.factory import Factory
# factory is to get instance of dynamic class (i.e. custom widget)

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
            # cities = [(d['name'], d['sys']['country']) for d in data['list']]
            cities = ["{} ({})".format(d['name'], d['sys']['country'])
                      for d in data['list']]
            self.search_results.item_strings = cities
            del self.search_results.adapter.data[:]
            # self.search_results.adapter.data.clear() #introduced in python3
            self.search_results.adapter.data.extend(cities)
            self.search_results._trigger_reset_populate()
        else:
            del self.search_results.adapter.data[:]
            # self.search_results.adapter.data.clear() #introduced in python3
            self.search_results.adapter.data.extend(None)
            self.search_results._trigger_reset_populate()

class LocationButton(ListItemButton):
    pass

class WeatherRoot(BoxLayout):
    addlocation = ObjectProperty()
    current_weather = ObjectProperty()

    def show_current_weather(self, location=None):
        self.clear_widgets()
        if location is None and self.current_weather is None:
            location = "New York (US)"
        if location is not None:
            self.current_weather = Factory.CurrentWeather()
            self.current_weather.location = location
        self.add_widget(self.current_weather)


    def show_add_location_form(self):
        self.clear_widgets()
        self.add_widget(self.addlocation)

class WeatherApp(App):
    pass

if __name__ == '__main__':
    WeatherApp().run()