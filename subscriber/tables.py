from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, LargeBinary, ForeignKey, DateTime
from sqlalchemy.sql import func

Base = declarative_base()


""" creating a common_map class for accessing the common_map objects and  attributes """


class common_map(Base):
    __tablename__ = 'commom_floormap'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60), unique=True)
    width = Column(Float)
    height = Column(Float)
    image = Column(LargeBinary)


""" creating a gateway_mastergateway class for accessing the gateway_mastergateway objects and  attributes """


class gateway_mastergateway(Base):
    __tablename__ = 'gateway_mastergateway'

    id = Column(Integer, primary_key=True, autoincrement=True)
    gatewayid = Column(String(20), unique=True)
    floor_id = Column(ForeignKey(common_map.id, ondelete='CASCADE'))
    lastseen = Column(DateTime(timezone=True), server_default=func.now())


""" creating a gateway_slavegateway class for accessing the gateway_slavegateway objects and  attributes """


class gateway_slavegateway(Base):
    __tablename__ = 'gateway_slavegateway'

    id = Column(Integer, primary_key=True, autoincrement=True)
    gatewayid = Column(String(20), unique=True)
    master_id = Column(ForeignKey(
        gateway_mastergateway.id, ondelete='CASCADE'))
    lastseen = Column(DateTime(timezone=True), server_default=func.now())


""" creating a asset_asset class for accessing the asset_asset objects and  attributes """


class employee_tag(Base):
    __tablename__ = 'employee_employeetag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tagid = Column(String(20), unique=True)
    battery = Column(Float)
    lastseen = Column(DateTime(timezone=True), server_default=func.now())
    x = Column(Float)
    y = Column(Float)
    floor_id = Column(ForeignKey(common_map.id, ondelete='CASCADE'))


class employee_registration(Base):
    __tablename__ = 'employee_employeeregistration'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    empid = Column(String(100))
    email = Column(String(254))
    phoneno = Column(String(12))
    address = Column(String(200))
    tagid_id = Column(ForeignKey(employee_tag.id, ondelete='CASCADE'))
    intime = Column(DateTime(timezone=True), server_default=func.now())


class employee_distancetracking(Base):
    __tablename__ = 'employee_distancetracking'

    id = Column(Integer, primary_key=True, autoincrement=True)
    distance = Column(Integer)
    tag1_id = Column(ForeignKey(employee_registration.id, ondelete='CASCADE'))
    tag2_id = Column(ForeignKey(employee_registration.id, ondelete='CASCADE'))
    timestamp = Column(DateTime(timezone=True))


""" creating a sensor_temperaturehumidity class for accessing the sensor_temperaturehumidity tables attributes """


class sensor_temperaturehumidity(Base):
    __tablename__ = 'sensor_temperaturehumidity'

    id = Column(Integer, primary_key=True, autoincrement=True)
    macid = Column(String(20))
    temperature = Column(Float)
    humidity = Column(Float)
    lastseen = Column(DateTime(timezone=True))
    x1 = Column(Float)
    y1 = Column(Float)
    x2 = Column(Float)
    y2 = Column(Float)
    floor_id = Column(ForeignKey(common_map.id, ondelete='CASCADE'))
    battery = Column(Float)


class sensor_dailytemperaturehumidity(Base):
    __tablename__ = 'sensor_dailytemperaturehumidity'

    id = Column(Integer, primary_key=True, autoincrement=True)
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime(timezone=True))
    asset_id = Column(ForeignKey(
        sensor_temperaturehumidity.id, ondelete='CASCADE'))


class sensor_weeklytemperaturehumidity(Base):
    __tablename__ = 'sensor_weeklytemperaturehumidity'

    id = Column(Integer, primary_key=True, autoincrement=True)
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime(timezone=True))
    asset_id = Column(ForeignKey(
        sensor_temperaturehumidity.id, ondelete='CASCADE'))


class sensor_monthlytemperaturehumidity(Base):
    __tablename__ = 'sensor_monthlytemperaturehumidity'

    id = Column(Integer, primary_key=True, autoincrement=True)
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime(timezone=True))
    asset_id = Column(ForeignKey(
        sensor_temperaturehumidity.id, ondelete='CASCADE'))


class sensor_iaq(Base):
    __tablename__ = 'sensor_iaq'

    id = Column(Integer, primary_key=True, autoincrement=True)
    macid = Column(String(20))
    lastseen = Column(DateTime(timezone=True))
    battery = Column(Float)
    co2 = Column(Float)
    floor_id = Column(ForeignKey(common_map.id, ondelete='CASCADE'))
    co2 = Column(Float)
    x = Column(Float)
    y = Column(Float)


class sensor_dailyiaq(Base):
    __tablename__ = "sensor_dailyiaq"

    id = Column(Integer, primary_key=True, autoincrement=True)
    co2 = Column(Float)
    co2 = Column(Float)
    timestamp = Column(DateTime(timezone=True))
    asset_id = Column(ForeignKey(sensor_iaq.id, ondelete='CASCADE'))


class sensor_weeklyiaq(Base):
    __tablename__ = "sensor_weeklyiaq"

    id = Column(Integer, primary_key=True, autoincrement=True)
    co2 = Column(Float)
    co2 = Column(Float)
    timestamp = Column(DateTime(timezone=True))
    asset_id = Column(ForeignKey(sensor_iaq.id, ondelete='CASCADE'))


class sensor_monthyiaq(Base):
    __tablename__ = "sensor_monthyiaq"

    id = Column(Integer, primary_key=True, autoincrement=True)
    co2 = Column(Float)
    co2 = Column(Float)
    timestamp = Column(DateTime(timezone=True))
    asset_id = Column(ForeignKey(sensor_iaq.id, ondelete='CASCADE'))


class signalrepeator(Base):
    __tablename__ = 'signalrepeator_signalrepeator'

    id = Column(Integer, primary_key=True, autoincrement=True)
    macid = Column(String(20))
    lastseen = Column(DateTime(timezone=True))


""" creating a alert_alert class for accessing the alert_alert tables attributes """


class alert_alert(Base):
    __tablename__ = 'alert_alert'

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    asset_id = Column(ForeignKey(employee_tag.id, ondelete='CASCADE'))


class zones_zones(Base):
    __tablename__ = 'zones_zones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    x1 = Column(Float)
    y1 = Column(Float)
    x2 = Column(Float)
    y2 = Column(Float)
    floor = Column(ForeignKey(common_map.id, ondelete='CASCADE'))


""" ZoneTracking model: """


class ZoneTracking(Base):
    __tablename__ = 'zones_zonetracking'

    id = Column(Integer, primary_key=True, autoincrement=True)
    zoneid_id = Column(ForeignKey(zones_zones.id, ondelete='CASCADE'))
    tagid_id = Column(ForeignKey(employee_registration.id, ondelete='CASCADE'))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
