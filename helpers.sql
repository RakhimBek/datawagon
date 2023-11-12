-- remove all dislocations hardly associated with the current set of STATIONS
select count(*)
from DISLOCATIONS
where STDISL not in (select ID from STATIONS);

-- remove all unsuited rows
delete
from DISLOCATIONS
where TRAININDEX not like '%-%';

-- parse index
ALTER TABLE DISLOCATIONS
    ADD DEPARTURE INTEGER;
ALTER TABLE DISLOCATIONS
    ADD DESTINATION INTEGER;
ALTER TABLE DISLOCATIONS
    ADD TRAINNUM INTEGER;

UPDATE DISLOCATIONS
SET DEPARTURE = substr(TRAININDEX, 0, instr(TRAININDEX, '-'));
UPDATE DISLOCATIONS
SET DEPARTURE = substr(TRAININDEX, 0, instr(TRAININDEX, '-'));
UPDATE DISLOCATIONS
SET TRAINNUM = substr(TRAININDEX, instr(TRAININDEX, '-') + 1);
UPDATE DISLOCATIONS
SET DESTINATION = substr(TRAINNUM, instr(TRAINNUM, '-') + 1);
UPDATE DISLOCATIONS
SET TRAINNUM = substr(TRAINNUM, 0, instr(TRAINNUM, '-'));


CREATE INDEX IF NOT EXISTS IDX_DEPARTURE ON DISLOCATIONS (DEPARTURE);
CREATE INDEX IF NOT EXISTS IDX_TRAINNUM ON DISLOCATIONS (TRAINNUM);
CREATE INDEX IF NOT EXISTS IDX_DESTINATION ON DISLOCATIONS (DESTINATION);


-- date of maximal activity in specified dislocation
select datetime(OPERDATE), count(*) as cc
from DISLOCATIONS
where STDISL == 9843
group by datetime(OPERDATE)
order by cc desc

select STDISL, (DISTINCT TRAINNUM) tt
from DISLOCATIONS
group by STDISL
order by tt desc;

-- duplications
select count(*)
from (
         SELECT WAGNUM,
                OPERDATE,
                STDISL,
                STDEST,
                TRAININDEX,
                DEPARTURE,
                DESTINATION,
                TRAINNUM,
                COUNT(*) AS CNT
         FROM DISLOCATIONS
         GROUP BY WAGNUM,
                  OPERDATE,
                  STDISL,
                  STDEST,
                  TRAININDEX,
                  DEPARTURE,
                  DESTINATION,
                  TRAINNUM
         HAVING COUNT(*) > 1);




-- trail of a train
select * from DISLOCATIONS where TRAINNUM=1 order by TRAINNUM, datetime(OPERDATE)
