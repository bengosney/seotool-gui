# Standard Library
import asyncio

# Third Party
import flet as ft
import pkg_resources
from seotool.crawl import Crawler

# First Party
from processors import ResultSet, hookimpl_processor


def get_engines() -> list[str]:
    engines = []
    for entry_point in pkg_resources.iter_entry_points("seo_engines"):
        engines.append(entry_point.name)
    return engines


def main(page: ft.Page):
    page.theme_mode = "dark"

    engines = get_engines()
    engine_group = ft.Column(
        [
            ft.Text("Engines:"),
            ft.RadioGroup(value=engines[0], content=ft.Column([ft.Radio(label=e, value=e) for e in engines])),
        ]
    )
    options_tab = ft.Tab(
        text="options",
        content=ft.Container(
            ft.Column(controls=[engine_group], expand=1),
            expand=1,
            padding=25,
        ),
    )

    site_input = ft.TextField(label="Site", value="https://www.stretchtheirlegs.co.uk/")
    log_list = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    log_tab = ft.Tab(text="Log", content=ft.Container(content=log_list))
    default_tabs = [
        options_tab,
        log_tab,
    ]
    tabs = ft.Tabs(
        animation_duration=300,
        expand=1,
        tabs=default_tabs,
    )

    class LogIt:
        @hookimpl_processor(tryfirst=True)
        def log(self, line, style):
            log_list.controls.append(ft.Text(line))
            page.update()
            return True

        @hookimpl_processor(tryfirst=True)
        def log_error(self, line):
            return self.log(line, "red")

        @hookimpl_processor()
        def process_output(self, resultsSets: list[ResultSet]):
            if tabs.tabs is None:
                return

            for result_set in resultsSets:
                if result_set.data is None or len(result_set.data) == 0:
                    continue

                grid = ft.ListView(spacing=25)
                headers = ft.Row(spacing=25)
                for header in result_set.data_headers:
                    headers.controls.append(ft.Text(header, expand=1))
                grid.controls.append(headers)

                for data_row in result_set.data:
                    row = ft.Row(spacing=25)
                    for header in result_set.data_headers:
                        row.controls.append(ft.Text(data_row[header], expand=1))
                    grid.controls.append(row)

                tabs.tabs.append(ft.Tab(text=result_set.title, content=grid))
            page.update()

    def button_clicked(e):
        log_list.controls = []
        tabs.tabs = default_tabs
        crawler = Crawler(url=f"{site_input.value}", ignore_robots=True)
        crawler.plugin_manager.register(LogIt(), "LogIt")

        asyncio.run(crawler.crawl())

    page.add(
        ft.Row(
            controls=[
                site_input,
                ft.ElevatedButton(text="Crawl", on_click=button_clicked),
            ]
        )
    )
    page.add(tabs)


ft.app(target=main)
