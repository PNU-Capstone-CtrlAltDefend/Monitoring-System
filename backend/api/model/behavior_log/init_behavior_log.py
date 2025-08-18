
from pathlib import Path
import pandas as pd

from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from datetime import datetime   

from model.database import engine, get_db, Base, SessionLocal

from model.security_manager import models as SecurityManager_models
from model.security_manager import crud as security_manager_crud
from model.security_manager import schemas as security_manager_schemas

from model.organization import models as Organization_models
from model.organization import crud as organization_crud
from model.organization import schemas as organization_schemas

from model.functional_unit import models as FunctionalUnit_models
from model.functional_unit import crud as functional_unit_crud

from model.department import models as Department_models    
from model.department import crud as department_crud

from model.team import models as Team_models
from model.team import crud as team_crud

from model.employee import models as Employee_models
from model.employee import crud as employee_crud

from model.pc import models as Pc_models
from model.pc import crud as pc_crud
from model.pc import schemas as pc_schemas

from model.router import models as Router_models
from model.router import crud as router_crud
from model.router import schemas as router_schemas

from model.behavior_log import models as BehaviorLog_models
from model.behavior_log import crud as behavior_log_crud
from model.behavior_log import schemas as behavior_logs_schemas

class BehaviorLogInserter:
    """
    행동 로그 seed data 초기화를 담당하는 클래스
    """
    def __init__(self, engine: engine, db: Annotated[Session, Depends(get_db)], organization_id: str, base_path: str = None):
        self.db = db
        self.engine = engine
        self.organization_id = organization_id
        self.base_path = base_path
        self.cutoff_dt = datetime(2011, 4, 28, 23, 59, 59) # last week ~ last - 3 week 

    def init_behavior_log(self):
        """
        전체 행동 로그 삽입 시퀀스 실행 메서드 
        """
        print("행동 로그 삽입: 1, 건너뛰기: 2")
        if input() == "2":
            return
        
        # 1. 디바이스 로그 데이터 삽입
        print("디바이스 로그 삽입: 2 건너뛰기: 1")
        if input() != "1":
            self.insert_device_log()

        # 2. http 로그 
        print("http 로그 삽입: 2 건너뛰기: 1")
        if input() != "1":
            self.insert_http_log() 

        # 3. 파일 로그
        print("파일 로그 삽입: 2 건너뛰기: 1")
        if input() != "1":
            self.insert_file_log()
        # 4. 로그온 로그
        print("로그온 로그 삽입: 2 건너뛰기: 1")
        if input() != "1":
            self.insert_logon_log()
        # 5. 이메일 로그 
        print("이메일 로그 삽입: 2 건너뛰기: 1")
        if input() != "1":
            self.insert_email_log()

    def insert_logon_log(self):
        """
        로그온 로그 삽입 메서드 
        """
        try:
            logon_csv = (Path(self.base_path) / "logon.csv")
            ldf = pd.read_csv(logon_csv)
            ldf["date_dt"] = pd.to_datetime(ldf["date"], format="%m/%d/%Y %H:%M:%S")

            print(ldf.head())
            itor = 0
            for row in reversed(list(ldf.itertuples(index = False))):
                itor += 1
                print(f"processing ittor: {itor}")
                if row.date_dt < self.cutoff_dt:    
                    break

                if not pc_crud.get_pc_by_id(self.db, row.pc):
                    pc_crud.create_pc(
                        self.db,
                        pc_schemas.PcsCreate(
                            pc_id=row.pc,
                            organization_id=self.organization_id,
                            ip_address="test",
                            mac_address="test",
                        ),
                    )
                
                logon_log_data = behavior_logs_schemas.BehaviorLogCreate(
                    event_id=row.id,
                    employee_id=row.user,
                    pc_id=row.pc,
                    timestamp=row.date_dt,  
                    event_type="device",
                    activity=row.activity,
                )
                behavior_log_crud.create_behavior_log(self.db, logon_log_data)
        except Exception as e:
            print(f"디바이스 로그 삽입 중 오류 발생: {e}")
        return
        
    def insert_device_log(self):
        """
        디바이스 로그 삽입 메서드 
        """
        try:
            device_csv = (Path(self.base_path) / "device.csv")
            ddf = pd.read_csv(device_csv)
            ddf["date_dt"] = pd.to_datetime(ddf["date"], format="%m/%d/%Y %H:%M:%S")    

            ddf = ddf.sort_values(by="date_dt")
            print (ddf.head())
            itor = 0
            for row in reversed(list(ddf.itertuples(index = False))):
                itor += 1
                print(f"processing ittor: {itor}")
                if row.date_dt < self.cutoff_dt:    
                    break

                if not pc_crud.get_pc_by_id(self.db, row.pc):
                    pc_crud.create_pc(
                        self.db,
                        pc_schemas.PcsCreate(
                            pc_id=row.pc,
                            organization_id=self.organization_id,
                            ip_address="test",
                            mac_address="test",
                        ),
                    )
                
                device_log_data = behavior_logs_schemas.BehaviorLogCreate(
                    event_id=row.id,
                    employee_id=row.user,
                    pc_id=row.pc,
                    timestamp=row.date_dt,  
                    event_type="device",
                    activity=row.activity,
                )
                behavior_log_crud.create_behavior_log(self.db, device_log_data)
        except Exception as e:
            print(f"디바이스 로그 삽입 중 오류 발생: {e}")
        return
    
    def insert_http_log(self):
        """
        http 로그 삽입 메서드
        """
        try:    
            http_csv = (Path(self.base_path) / "http.csv")  
            hdf = pd.read_csv(http_csv)
            hdf["date_dt"] = pd.to_datetime(hdf["date"], format="%m/%d/%Y %H:%M:%S")
            hdf = hdf.sort_values(by="date_dt")
            print(hdf.head())

            itor = 0
            for row in reversed(list(hdf.itertuples(index = False))):
                itor += 1
                print(f"processing ittor: {itor}")
                if row.date_dt < self.cutoff_dt:    
                    break
                
                if not pc_crud.get_pc_by_id(self.db, row.pc):
                    pc_crud.create_pc(
                        self.db,
                        pc_schemas.PcsCreate(
                            pc_id=row.pc,
                            organization_id=self.organization_id,
                            ip_address="test",
                            mac_address="test",
                        ),
                    )

                http_log_data = behavior_logs_schemas.BehaviorLogCreate(
                    event_id=row.id,
                    employee_id=row.user,
                    pc_id=row.pc,
                    timestamp=row.date_dt,  
                    event_type="http",
                    url=row.url,
                )
                behavior_log_crud.create_behavior_log(self.db, http_log_data)

        except Exception as e:
            print(f"HTTP 로그 삽입 중 오류 발생: {e}")
        return
    def insert_file_log(self):
        """
        파일 로그 삽입 메서드 
        """
        try:
            file_csv = (Path(self.base_path) / "file.csv")
            fdf = pd.read_csv(file_csv)
            fdf["date_dt"] = pd.to_datetime(fdf["date"], format="%m/%d/%Y %H:%M:%S")
            fdf = fdf.sort_values(by="date_dt")
            print(fdf.head())

            itor = 0
            for row in reversed(list(fdf.itertuples(index = False))):
                itor += 1
                print(f"processing ittor: {itor}")
                if row.date_dt < self.cutoff_dt:    
                    break
                
                if not pc_crud.get_pc_by_id(self.db, row.pc):
                    pc_crud.create_pc(
                        self.db,
                        pc_schemas.PcsCreate(
                            pc_id=row.pc,
                            organization_id=self.organization_id,
                            ip_address="test",
                            mac_address="test",
                        ),
                    )

                file_log_data = behavior_logs_schemas.BehaviorLogCreate(
                    event_id=row.id,
                    employee_id=row.user,
                    pc_id=row.pc,
                    timestamp=row.date_dt,  
                    event_type="file",
                    filename=row.filename,
                )
                behavior_log_crud.create_behavior_log(self.db, file_log_data)

        except Exception as e:
            print(f"파일 로그 삽입 중 오류 발생: {e}")
    
    def insert_email_log(self):
        """
        이메일 로그 삽입 메서드 
        """
        try: 
            email_csv = (Path(self.base_path) / "email.csv")    
            edf = pd.read_csv(email_csv)    
            edf["date_dt"] = pd.to_datetime(edf["date"], format="%m/%d/%Y %H:%M:%S")    
            edf.rename(columns={"from": "from_addr"}, inplace=True)
            edf = edf.sort_values(by="date_dt")
            print(edf.head())

            itor = 0
            for row in reversed(list(edf.itertuples(index = False))):
                itor += 1
                print(f"processing ittor: {itor}")
                if row.date_dt < self.cutoff_dt:    
                    break
                
                if not pc_crud.get_pc_by_id(self.db, row.pc):
                    pc_crud.create_pc(
                        self.db,
                        pc_schemas.PcsCreate(
                            pc_id=row.pc,
                            organization_id=self.organization_id,
                            ip_address="test",
                            mac_address="test",
                        ),
                    )

                file_log_data = behavior_logs_schemas.BehaviorLogCreate(
                    event_id=row.id,
                    employee_id=row.user,
                    pc_id=row.pc,
                    timestamp=row.date_dt,  
                    event_type="email",
                    to = row.to,
                    cc = row.cc,
                    bcc = row.bcc,
                    from_addr = row.from_addr,
                    size = row.size,    
                    attachment = row.attachments,
                )
                behavior_log_crud.create_behavior_log(self.db, file_log_data)

        except Exception as e:
            print(f"이메일 로그 삽입 중 오류 발생: {e}")


base_path = (Path(__file__).resolve().parent.parent / "dataset" / "behavior_log" )
loginserter = BehaviorLogInserter(engine, SessionLocal(), organization_id="d038bcfa-08aa-4c40-a3e8-0fd73dbd6436", base_path=base_path)

loginserter.init_behavior_log()

