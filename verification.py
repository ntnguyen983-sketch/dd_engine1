"""S11 verification and confidence scoring."""
from __future__ import annotations
from dataclasses import dataclass
from pgl import clamp
from sie import KhiVector

@dataclass
class LevelScore:
    level:str; score:float; ghi_chu:str

def level0_ban_the(khi):
    ok=0.0<=khi.S<=1.0 and -1.0<=khi.D<=1.0 and 0.0<=khi.I<=1.0
    return LevelScore("Level 0 - Bản thể",1.0 if ok else 0.3,"Kiểm tra ràng buộc miền giá trị PGL (A1).")
def level1_do_luong(khi,graph_edge_count): return LevelScore("Level 1 - Đo lường",clamp(0.4+0.1*min(6,graph_edge_count),0.0,1.0),f"Số liên kết SIE quan sát được: {graph_edge_count}.")
def level2_dong_luc(khi): return LevelScore("Level 2 - Động lực",clamp(1.0-abs(khi.I-khi.F),0.0,1.0),"Đối chiếu nhất quán I và F.")
def level3_can_thiep(has_actionable_nodes): return LevelScore("Level 3 - Can thiệp",0.7 if has_actionable_nodes else 0.4,"Actionable Nodes khả dụng cho phân tích can thiệp." if has_actionable_nodes else "Chưa xác định Actionable Node.")
def level4_tong_quat_hoa(history_len): return LevelScore("Level 4 - Tổng quát hóa",clamp(0.3+0.05*min(14,history_len),0.0,1.0),f"Số chu kỳ lịch sử tích lũy: {history_len}.")
def confidence_score(levels,level_weights):
    key_map={"Level 0 - Bản thể":"level0_ban_the","Level 1 - Đo lường":"level1_do_luong","Level 2 - Động lực":"level2_dong_luc","Level 3 - Can thiệp":"level3_can_thiep","Level 4 - Tổng quát hóa":"level4_tong_quat_hoa"}
    return clamp(sum(level_weights.get(key_map[x.level],0.2)*x.score for x in levels),0.0,1.0)
def self_correction_notes(confidence):
    notes=[]
    if confidence<0.5: notes += ["C < 0.5: đề xuất hiệu chỉnh Level 3 - rà soát lại Trọng số Ngưỡng (config.json).","C < 0.5: đề xuất hiệu chỉnh Level 2 - kiểm tra Bản đồ Ánh xạ S03 (Structural Mapping)."]
    if confidence<0.3: notes.append("C < 0.3: đề xuất hiệu chỉnh Level 2 - rà soát Ma trận Trực quan Đại quái (S08).")
    return notes
