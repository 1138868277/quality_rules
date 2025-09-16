--分级诊断_光伏_死值
insert into import_list_sz
(
	module_source 
	,energy_type
	,standard_name
	,sz_threshold
	,sz_windows
	,sliding_step
	,begin_time
	,end_time
	,measure_name
	,cd_code
)
with cd_data as (
		select  
			cd_code 					as cd_code
			,cd_name					as cd_name
			,left(cd_code,4) 			as station_code
			,substring(cd_code,5,1) 	as energy_type
			,right(cd_code,5) 			as measure_code
			,substring(cd_code,13,3)	as second_code
		from 
			measure_data 
		where 
			substring(cd_code,5,1)='G' -- 光伏
		and substring(cd_code,13,3)='002' -- 光伏发电系统
		and substring(cd_code,20,3) in ('003','005') -- 组串式逆变器和直流汇流箱
	union all 
		select  
			cd_code 					as cd_code
			,cd_name					as cd_name
			,left(cd_code,4) 			as station_code
			,substring(cd_code,5,1) 	as energy_type
			,right(cd_code,5) 			as measure_code
			,substring(cd_code,13,3)	as second_code
		from 
			measure_data 
		where 
			substring(cd_code,5,1)='G' -- 光伏
		and substring(cd_code,13,3)='004' -- 光功率预测系统
),standard_data as (
	select 
	*
	from 
	通用.standard_list
	where 
		module_source = '分级诊断'
	and energy_type = '光伏'
),final_data as (
	select 
		t1.cd_name
		,t1.cd_code
		,t3.station_name
		,t2.second_name
		,t2.measure_code
		,t2.measure_name
		,t2.module_source
		,t2.energy_type
		,tb_windows
		,ss_windows
		,ss_threshold
		,yx_range
		,zd_duration
	from 
		cd_data t1
	inner join 
		standard_data t2 
	on 
		t1.measure_code=t2.measure_code and t1.second_code = t2.second_code
	inner join 
		dim_station t3 
	on
		t1.station_code=t3.station_code
)
select 
distinct
module_source
,energy_type
,concat(station_name,'_',module_source,'_',second_name,'_',measure_name,'_死值')as standard_name
,coalesce(ss_threshold::float,0) as sz_threshold
,ss_windows::float as sz_windows
,ss_windows::float/2 as sliding_step
,'0:00' as begin_time
,'23:59' as end_time
,measure_name
,cd_code
from  
	final_data
where 
	ss_windows !=''
order by measure_name;