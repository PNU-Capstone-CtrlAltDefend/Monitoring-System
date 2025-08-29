from sqlalchemy.orm import Session

from model.pc.crud import set_pc_current_state_and_present_user_id_by_pc_id
from model.pc.models import LogonState

from model.employee.crud import get_anomaly_flag_by_employee_id

from services.network_controller.pc_access_control_service import NetworkAccessController

class LogonProcessor:
    """
    로그온/오프 로그를 받아, 해당하는 PC의 상태를 업데이트 하고 
    만약 이상 사용자의 로그온이 감지될 경우 네트워크 차단을 요청 및 이메일 전송, 알림을 보이는 클래스 
    """
    def __init__(self, db: Session, log_data):
        self.db=db
        self.log_data=log_data
    
    def run(self):
        print("LogonProcessor called with log_data:", self.log_data)
        try: 
            # 1. PC 상태 업데이트 
            self._update_pc_state()
            print(f"PC 상태가 성공적으로 업데이트되었습니다: {self.log_data.pc_id}, {self.log_data.activity}")

            # 2. 로그온한 사용자의 악성 여부 확인 
            if get_anomaly_flag_by_employee_id(self.db, self.log_data.employee_id) and self.log_data.activity == "logon":
                print(f"악성 사용자의 로그온이 감지 되었습니다: {self.log_data.employee_id}")

                # 2.1 악성 사용자일 경우, 호출 
                self._handle_anomaly_logon()
            # 악성이 아닐 경우, 추가 조치 없이 종료
            return 
        except Exception as e:  
            print(f"PC 상태 업데이트 중 오류 발생 {e}")
            return 

    def _update_pc_state(self):
        pc_id = self.log_data.pc_id
        state = self.log_data.activity
        if state == "logon":
            current_state = LogonState.ON
        elif state == "logoff":
            current_state = LogonState.OFF
        employee_id = self.log_data.employee_id

        if not pc_id:
            return
        
        set_pc_current_state_and_present_user_id_by_pc_id(
            self.db, pc_id, current_state, employee_id
        )
    
    def _handle_anomaly_logon(self):
        # 1. 네트워크 차단 요청 
        result = NetworkAccessController(self.db, self.log_data.pc_id, access_flag=False).run()
        if(result):
            print(f"네트워크 차단이 성공적으로 완료되었습니다.: {self.log_data.pc_id}")
        # 2. 관리자 이메일 전송

        # 3. 관리자 알림 
        pass
