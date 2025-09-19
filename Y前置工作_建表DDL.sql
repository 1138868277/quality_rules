-- 创建模式
CREATE SCHEMA "云南区域";
CREATE SCHEMA "通用";

-- 创建表
CREATE TABLE 云南区域.dim_station (
	station_code text NULL,
	station_name text NULL
);

CREATE TABLE 云南区域.import_list_sz (
	module_source text NULL,
	energy_type text NULL,
	standard_name text NULL,
	sz_threshold float8 NULL,
	sz_windows float8 NULL,
	sliding_step float8 NULL,
	begin_time text NULL,
	end_time text NULL,
	measure_name text NULL,
	cd_code text NULL
);

CREATE TABLE 云南区域.import_list_tb (
	module_source text NULL,
	energy_type text NULL,
	standard_name text NULL,
	tb_windows float8 NULL,
	sliding_step float8 NULL,
	begin_time text NULL,
	end_time text NULL,
	measure_name text NULL,
	cd_code text NULL
);

CREATE TABLE 云南区域.import_list_yx (
	module_source text NULL,
	energy_type text NULL,
	standard_name text NULL,
	upper_range float8 NULL,
	lower_range float8 NULL,
	begin_time text NULL,
	end_time text NULL,
	measure_name text NULL,
	cd_code text NULL
);

CREATE TABLE 云南区域.import_list_zd (
	module_source text NULL,
	energy_type text NULL,
	standard_name text NULL,
	zd_duration float8 NULL,
	begin_time text NULL,
	end_time text NULL,
	measure_name text NULL,
	cd_code text NULL
);

CREATE TABLE 云南区域.measure_data (
	cd_code text NULL,
	cd_name text NULL
);


-- 在通用模式中创建标准维表,然后将【稽核标准参考文档/终版_时序数据质量稽核标准.sql】中的标准导入到表中
CREATE TABLE 通用.standard_list (
	energy_type text NULL,
	module_source text NULL,
	second_code text NULL,
	second_name text NULL,
	measure_code text NULL,
	measure_name text NULL,
	tb_windows text NULL,
	ss_windows text NULL,
	ss_threshold text NULL,
	yx_range text NULL,
	zd_duration text NULL
);
