# Cache Gather
A web based for collecting hydrologic field observations.  This application uses a cloud-based PostgreSQL server, and uses an isolated python script to assess, validate, and upload data to a local server.


### sql.py
#### get_engine
creates a sqlalchemy engine via the local or web method
use conn = engine.raw_connection() for conn
#### get_field_observations
gets field observations from database table field_observations
#### get site list
returns a list of active sites from database table sites

### database
#### observations
site                    text
datetime                text
observation             text
notes                   text
#### sites
site_sql_id             bigint
site_number             text
site_name               text
latitude                double precision
longitude               double precision
comment                 text
gauge_type              text
reference_elevation     double precision
reference_information   text

