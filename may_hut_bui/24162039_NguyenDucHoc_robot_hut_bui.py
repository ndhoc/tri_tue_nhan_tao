import random

class may_hut_bui:
    def __init__(self):
        self.bo_nho_ban_do = {'A': 'Chưa biết', 'B': 'Chưa biết'}
        self.vi_tri_hien_tai = 'A'
        self.vong_lap_da_chay = 0
        
    def cap_nhat_trang_thai(self, cam_bien_vi_tri, cam_bien_bui, co_vat_can):
        # Cập nhật những gì vừa nhìn thấy vào bộ nhớ
        self.vi_tri_hien_tai = cam_bien_vi_tri
        self.bo_nho_ban_do[cam_bien_vi_tri] = cam_bien_bui
        
        if co_vat_can:
            return True
        return False

    def chon_hanh_dong(self, bi_vuong_vat_can):
        tinh_trang_cho_nay = self.bo_nho_ban_do[self.vi_tri_hien_tai]

        if tinh_trang_cho_nay == 'Ban':
            return 'Hui bui'

        if bi_vuong_vat_can:
            return 'Quay dau hoac re huong'

        # Luật 3: Nếu sạch rồi thì đi sang phòng khác
        if self.vi_tri_hien_tai == 'A':
            return "di sang phai"
        else:
            return "di sang trai"

mhb = may_hut_bui()

# May hut bui o phong A, phòng A ban, và có vat can di duong sang B
nhan_thuc_tu_cam_bien = ('A', 'Ban', True) 

print(f"May hut bui o vi tri: {nhan_thuc_tu_cam_bien[0]}")
co_vat_can = mhb.cap_nhat_trang_thai('A', 'Ban', True)
hanh_dong = mhb.chon_hanh_dong(co_vat_can)
print(f"=> May hut bui se: {hanh_dong}")

print("-" * 67)

# Neu khi hut xong, phong A sach, muon sang B nhung gap vat can
co_vat_can = mhb.cap_nhat_trang_thai('A', 'Sach', True)
hanh_dong = mhb.chon_hanh_dong(co_vat_can)
print(f"=> May hut bui se: {hanh_dong}")