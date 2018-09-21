import datetime as dt
from recargas.models import Direccion
import pandas as pd

def safe_map(m, d):
    return m.get(d) if d else None

class ETL:
    
    def __init__(self, dir, reset=False, subsample=None, batch_size=2000):
        self.dir = dir
        self.subsample = subsample
        self.mapping = {}
        self.start_time = None
        self.batch_size = batch_size
        self.reset = reset
        # self.ventas = Ventas.objects.first()

    #    def clear_database(self):
    #     self.log("Clearing database")
    #     call_command("flush", interactive=False)


       def log(self, message):
        if self.start_time:
            current_time = dt.datetime.now()
            period = current_time - self.start_time
        else:
            period = dt.timedelta(0)
            print("[{:7.2f}] {}".format(period.total_seconds(), message))


        def map(self, model_name, value):
        return safe_map(self.mapping[model_name], value)    

    

    def run(self):
        self.start_time = dt.datetime.now()

        if self.reset:
            self.clear_database()

        self.ventas = self.load_recargas.py
        self.mapping['Direccion'] = self.create_from_ventas(column="Dirección",
                                                            model=Direccion,
                                                            to_field="direccion_id")

    def create_from_ventas(self, column, model, to_field):
        self.log()


    #  def load_ventas(self):
    #     self.log("Cargando ventas...")

    #     filename = os.path.join(self.dir, "P2P201708.xlsx")
    #     xlsx = pd.ExcelFile(filename)
    #     df = pd.read_excel(xlsx, encoding='ISO-8859-1',
    #                      dtype={"streetno": "object"})
    #     strip_dataframe(df)

    #     if self.subsample:
    #         df = df.sample(frac=self.subsample)

    #     df = self.exclude_existing(df, Venta, 'inci_id', 'venta_id')

    #     return df
