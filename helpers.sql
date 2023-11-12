-- remove all dislocations hardly associated with the current set of STATIONS
select count(*) from DISLOCATIONS where STDISL not in (select ID from STATIONS);

-- remove all unsuited rows
delete from DISLOCATIONS where TRAININDEX not like '%-%';