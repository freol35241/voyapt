from pathlib import Path
import cdsapi

YEARS = [2019]
MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

ROOT = Path("wind_data")
ROOT.mkdir(exist_ok=True)

c = cdsapi.Client(key="YOUR_API_KEY")

for year in YEARS:
    for month in MONTHS:
        month = str(month).zfill(2)
        c.retrieve(
            "reanalysis-era5-single-levels",
            {
                "product_type": "reanalysis",
                "format": "netcdf",
                "variable": [
                    "10m_u_component_of_wind",
                    "10m_v_component_of_wind",
                ],
                "year": str(year),
                "month": month,
                "day": [
                    "01",
                    "02",
                    "03",
                    "04",
                    "05",
                    "06",
                    "07",
                    "08",
                    "09",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                    "26",
                    "27",
                    "28",
                    "29",
                    "30",
                    "31",
                ],
                "time": [
                    "00:00",
                    "06:00",
                    "12:00",
                    "18:00",
                ],
            },
            str(ROOT / f"CDS_wind_{year}_{month}.nc"),
        )
