import json
import asyncio
import re
import datetime
import os


import aiohttp


class Downloader(object):

    def __init__(self, urls):
        self.urls = urls
        self._htmls = []
        self.time_temp_dict = {}

    async def download_single_page(self, url):
        async with aiohttp.ClientSession() as session:
            # set proxy to backup
            try:
                async with session.get(url) as resp:
                    self._htmls.append((re.search('\d+', url).group(), await resp.text()))

            except aiohttp.client_exceptions.ClientConnectorError:
                async with session.get(url, proxy="http://10.67.19.104:8989") as resp:
                    self._htmls.append((re.search('\d+', url).group(), await resp.text()))


    def download(self):
        print('downloading  ..........')
        # loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [self.download_single_page(url) for url in self.urls]
        loop.run_until_complete(asyncio.wait(tasks))
        print('download finished ! ')

    @property
    def htmls(self):
        self.download()
        return self._htmls


def compose_weather_date_link():
    link = "http://www.tianqihoubao.com/lishi/dongli/month/{}.html"
    links_dict = {}

    for year in range(2011, 2019):
        link_year_list = []
        for month in range(1, 13):
            date = str(year) + str('{:0>2d}'.format(month))
            tmp_link = link.format(date)
            link_year_list.append(tmp_link)
        links_dict[str(year)] = link_year_list

    return links_dict


def parse_html(html):
    pattern = re.compile('<tr>.*?<td>\s*<a href=.*?dongli/(.*?).ht.*? title=.*?>.*?</a>\s*</td>.*?<td>.*?</td>.*?'
                         '<td>(.*?)</td>.*?<td>.*?</td>.*?</tr>', re.S)
    result = re.findall(pattern, html)
    csv_list = []

    for row_content in result:
        tmp_row_list = []
        for unit in row_content:
            tmp_row_list.append(re.sub(r'/', ' ', re.sub(r'℃|\s*', '', unit)))
        tmp = tmp_row_list[1].split()
        avg = 0
        for x in tmp:
            if x.startswith('-'):
                x = -1 * int(x)
            else:
                x = int(x)
            avg += x
        tmp_row_list[1] = avg/2
        csv_list.append(tmp_row_list)
    return csv_list


def store_data(**link_dict):
    time_temp = {}
    total_links = []
    for value in link_dict.values():
        total_links.extend(value)
    # for key in link_dict.keys():
    # print(total_links)
    downloader_html = Downloader(total_links).htmls
    html_dict = dict(downloader_html)

    data_set = []

    for key in html_dict.keys():
        value = parse_html(html_dict[key])
        time_temp[key] = dict(value)

        for date_time, temp in value:
            data_set.append({"time": date_time, "value": temp})

    data_set.sort(key=lambda x: x["time"])

    dir_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(dir_path, "dongli_history_temperature.json"), 'w')as fp:
        json.dump(data_set, fp)

    return time_temp


class WeatherCrawler:
    def __init__(self):
        self.time_temp_dict = {}

    def temp_crawler(self):
        start_time = datetime.datetime.now()
        dongli_link_dict = compose_weather_date_link()
        time_temp_dict = store_data(**dongli_link_dict)
        endtime = datetime.datetime.now()
        differtime = endtime - start_time
        print('download last for {} s'.format(differtime.seconds))
        self.time_temp_dict = time_temp_dict


if __name__ == '__main__':
    data_downloader = WeatherCrawler()
    data_downloader.temp_crawler()
