"""Synthetic rc2 payload header for publisher verification."""
HEADER = (
    "# dataset: GeoCSV 2.0\n# schema: MERMAID GeoCSV v1.0.0-rc2\n"
    "# created: 2026-10-29T00:00:00.000000Z\n# delimiter: ,\n# lineterminator: \\n\n"
    "# field_type: string,datetime,datetime,string,string,string,string,string,float,float,float,float,float,float,float,integer,float,float\n"
    "# field_unit: unitless,iso8601,iso8601,unitless,unitless,unitless,unitless,unitless,degrees_north,degrees_east,degrees_north,degrees_east,mbar,mbar,hertz,unitless,seconds,seconds\n"
    "type,measured_time,derived_time,network,station,location,channel,data_quality,measured_latitude,measured_longitude,estimated_latitude,estimated_longitude,measured_pressure,estimated_pressure,sample_rate,sample_count,clock_offset,time_correction_applied\n"
)
