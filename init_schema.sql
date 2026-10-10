-- DROP SCHEMA public;

-- Schema public already created by PostgreSQL by default.
-- Granting usage to the app user.
GRANT ALL ON SCHEMA public TO app;

-- DROP SEQUENCE public.anh_thu_vien_id_seq;

CREATE SEQUENCE public.anh_thu_vien_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.bai_viet_id_seq;

CREATE SEQUENCE public.bai_viet_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.bao_cao_id_seq;

CREATE SEQUENCE public.bao_cao_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.hinh_anh_tin_dang_id_seq;

CREATE SEQUENCE public.hinh_anh_tin_dang_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.loai_bat_dong_san_id_seq;

CREATE SEQUENCE public.loai_bat_dong_san_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.nguoi_dung_id_seq;

CREATE SEQUENCE public.nguoi_dung_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.phuong_xa_id_seq;

CREATE SEQUENCE public.phuong_xa_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.phuong_xa_moi_id_seq;

CREATE SEQUENCE public.phuong_xa_moi_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.quan_huyen_id_seq;

CREATE SEQUENCE public.quan_huyen_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.tien_ich_id_seq;

CREATE SEQUENCE public.tien_ich_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.tin_dang_ban_cho_id_seq;

CREATE SEQUENCE public.tin_dang_ban_cho_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.tin_dang_id_seq;

CREATE SEQUENCE public.tin_dang_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.tin_yeu_thich_id_seq;

CREATE SEQUENCE public.tin_yeu_thich_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.tinh_thanh_id_seq;

CREATE SEQUENCE public.tinh_thanh_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;-- public.alembic_version definition

-- Drop table

-- DROP TABLE public.alembic_version;

CREATE TABLE public.alembic_version ( version_num varchar(32) NOT NULL, CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num));


-- public.loai_bat_dong_san definition

-- Drop table

-- DROP TABLE public.loai_bat_dong_san;

CREATE TABLE public.loai_bat_dong_san ( id serial4 NOT NULL, ten varchar(100) NOT NULL, mo_ta varchar(255) NULL, trang_thai varchar(20) DEFAULT 'HOAT_DONG'::character varying NOT NULL, CONSTRAINT loai_bat_dong_san_pkey PRIMARY KEY (id), CONSTRAINT loai_bat_dong_san_ten_key UNIQUE (ten));


-- public.nguoi_dung definition

-- Drop table

-- DROP TABLE public.nguoi_dung;

CREATE TABLE public.nguoi_dung ( id serial4 NOT NULL, ho_ten varchar(150) NOT NULL, email varchar(150) NOT NULL, mat_khau_hash varchar(255) NOT NULL, so_dien_thoai varchar(20) NULL, vai_tro varchar(20) NOT NULL, trang_thai varchar(20) NOT NULL, ngay_tao timestamptz DEFAULT now() NOT NULL, ngay_cap_nhat timestamptz DEFAULT now() NOT NULL, CONSTRAINT nguoi_dung_pkey PRIMARY KEY (id));
CREATE UNIQUE INDEX ix_nguoi_dung_email ON public.nguoi_dung USING btree (email);


-- public.tien_ich definition

-- Drop table

-- DROP TABLE public.tien_ich;

CREATE TABLE public.tien_ich ( id serial4 NOT NULL, ten varchar(100) NOT NULL, CONSTRAINT tien_ich_pkey PRIMARY KEY (id), CONSTRAINT tien_ich_ten_key UNIQUE (ten));


-- public.tinh_thanh definition

-- Drop table

-- DROP TABLE public.tinh_thanh;

CREATE TABLE public.tinh_thanh ( id serial4 NOT NULL, ten varchar(100) NOT NULL, CONSTRAINT tinh_thanh_pkey PRIMARY KEY (id), CONSTRAINT tinh_thanh_ten_key UNIQUE (ten));


-- public.anh_thu_vien definition

-- Drop table

-- DROP TABLE public.anh_thu_vien;

CREATE TABLE public.anh_thu_vien ( id serial4 NOT NULL, nguoi_dung_id int4 NOT NULL, ten_doi_tuong varchar(255) NOT NULL, duong_dan_anh varchar(500) NOT NULL, ten_tep_goc varchar(255) NOT NULL, dung_luong int4 NOT NULL, ngay_tai_len timestamptz DEFAULT now() NOT NULL, CONSTRAINT anh_thu_vien_pkey PRIMARY KEY (id), CONSTRAINT anh_thu_vien_nguoi_dung_id_fkey FOREIGN KEY (nguoi_dung_id) REFERENCES public.nguoi_dung(id));


-- public.bai_viet definition

-- Drop table

-- DROP TABLE public.bai_viet;

CREATE TABLE public.bai_viet ( id serial4 NOT NULL, tieu_de varchar(200) NOT NULL, slug varchar(220) NOT NULL, tom_tat varchar(200) NOT NULL, noi_dung_html text NOT NULL, anh_bia_id int4 NULL, trang_thai varchar(20) DEFAULT 'NHAP'::character varying NOT NULL, nguoi_tao_id int4 NOT NULL, luot_xem int4 DEFAULT 0 NOT NULL, ngay_dang timestamptz NULL, created_at timestamptz DEFAULT now() NOT NULL, updated_at timestamptz DEFAULT now() NOT NULL, CONSTRAINT bai_viet_pkey PRIMARY KEY (id), CONSTRAINT bai_viet_anh_bia_id_fkey FOREIGN KEY (anh_bia_id) REFERENCES public.anh_thu_vien(id), CONSTRAINT bai_viet_nguoi_tao_id_fkey FOREIGN KEY (nguoi_tao_id) REFERENCES public.nguoi_dung(id));
CREATE UNIQUE INDEX ix_bai_viet_slug ON public.bai_viet USING btree (slug);


-- public.phuong_xa_moi definition

-- Drop table

-- DROP TABLE public.phuong_xa_moi;

CREATE TABLE public.phuong_xa_moi ( id serial4 NOT NULL, ten varchar(100) NOT NULL, ma_hanh_chinh varchar(20) NOT NULL, tinh_thanh_id int4 NOT NULL, CONSTRAINT phuong_xa_moi_ma_hanh_chinh_key UNIQUE (ma_hanh_chinh), CONSTRAINT phuong_xa_moi_pkey PRIMARY KEY (id), CONSTRAINT phuong_xa_moi_tinh_thanh_id_fkey FOREIGN KEY (tinh_thanh_id) REFERENCES public.tinh_thanh(id));


-- public.quan_huyen definition

-- Drop table

-- DROP TABLE public.quan_huyen;

CREATE TABLE public.quan_huyen ( id serial4 NOT NULL, ten varchar(100) NOT NULL, tinh_thanh_id int4 NOT NULL, CONSTRAINT quan_huyen_pkey PRIMARY KEY (id), CONSTRAINT quan_huyen_tinh_thanh_id_fkey FOREIGN KEY (tinh_thanh_id) REFERENCES public.tinh_thanh(id));


-- public.phuong_xa definition

-- Drop table

-- DROP TABLE public.phuong_xa;

CREATE TABLE public.phuong_xa ( id serial4 NOT NULL, ten varchar(100) NOT NULL, quan_huyen_id int4 NOT NULL, ma_hanh_chinh varchar(20) NULL, CONSTRAINT phuong_xa_pkey PRIMARY KEY (id), CONSTRAINT uq_phuong_xa_ma_hanh_chinh UNIQUE (ma_hanh_chinh), CONSTRAINT phuong_xa_quan_huyen_id_fkey FOREIGN KEY (quan_huyen_id) REFERENCES public.quan_huyen(id));


-- public.phuong_xa_anh_xa definition

-- Drop table

-- DROP TABLE public.phuong_xa_anh_xa;

CREATE TABLE public.phuong_xa_anh_xa ( phuong_xa_id int4 NOT NULL, phuong_xa_moi_id int4 NOT NULL, CONSTRAINT phuong_xa_anh_xa_pkey PRIMARY KEY (phuong_xa_id, phuong_xa_moi_id), CONSTRAINT phuong_xa_anh_xa_phuong_xa_id_fkey FOREIGN KEY (phuong_xa_id) REFERENCES public.phuong_xa(id), CONSTRAINT phuong_xa_anh_xa_phuong_xa_moi_id_fkey FOREIGN KEY (phuong_xa_moi_id) REFERENCES public.phuong_xa_moi(id));


-- public.tin_dang definition

-- Drop table

-- DROP TABLE public.tin_dang;

CREATE TABLE public.tin_dang ( id serial4 NOT NULL, tieu_de varchar(150) NOT NULL, mo_ta text NOT NULL, gia_thue numeric(14, 2) NOT NULL, dien_tich numeric(8, 2) NOT NULL, dia_chi_chi_tiet varchar(255) NOT NULL, loai_bat_dong_san_id int4 NOT NULL, phuong_xa_id int4 NOT NULL, nguoi_dang_id int4 NOT NULL, ten_nguoi_lien_he varchar(100) NOT NULL, so_dien_thoai_lien_he varchar(20) NOT NULL, phuong_thuc_lien_he_uu_tien varchar(20) NOT NULL, trang_thai varchar(20) NOT NULL, ly_do_khoa varchar(255) NULL, luot_xem int4 NOT NULL, ngay_dang timestamptz DEFAULT now() NOT NULL, ngay_cap_nhat timestamptz DEFAULT now() NOT NULL, phong_ngu int4 NOT NULL, phong_tam int4 NOT NULL, is_blocked bool DEFAULT false NOT NULL, is_deleted bool DEFAULT false NOT NULL, deleted_at timestamptz NULL, CONSTRAINT tin_dang_pkey PRIMARY KEY (id), CONSTRAINT tin_dang_loai_bat_dong_san_id_fkey FOREIGN KEY (loai_bat_dong_san_id) REFERENCES public.loai_bat_dong_san(id), CONSTRAINT tin_dang_nguoi_dang_id_fkey FOREIGN KEY (nguoi_dang_id) REFERENCES public.nguoi_dung(id), CONSTRAINT tin_dang_phuong_xa_id_fkey FOREIGN KEY (phuong_xa_id) REFERENCES public.phuong_xa(id));


-- public.tin_dang_ban_cho definition

-- Drop table

-- DROP TABLE public.tin_dang_ban_cho;

CREATE TABLE public.tin_dang_ban_cho ( id serial4 NOT NULL, tin_dang_id int4 NOT NULL, tieu_de varchar(150) NOT NULL, mo_ta text NOT NULL, gia_thue numeric(14, 2) NOT NULL, dien_tich numeric(8, 2) NOT NULL, phong_ngu int4 NOT NULL, phong_tam int4 NOT NULL, dia_chi_chi_tiet varchar(255) NOT NULL, loai_bat_dong_san_id int4 NOT NULL, phuong_xa_id int4 NOT NULL, ten_nguoi_lien_he varchar(100) NOT NULL, so_dien_thoai_lien_he varchar(20) NOT NULL, phuong_thuc_lien_he_uu_tien varchar(20) NOT NULL, tien_ich_ten json NOT NULL, hinh_anh json NOT NULL, ngay_gui timestamptz DEFAULT now() NOT NULL, CONSTRAINT tin_dang_ban_cho_pkey PRIMARY KEY (id), CONSTRAINT tin_dang_ban_cho_tin_dang_id_key UNIQUE (tin_dang_id), CONSTRAINT tin_dang_ban_cho_loai_bat_dong_san_id_fkey FOREIGN KEY (loai_bat_dong_san_id) REFERENCES public.loai_bat_dong_san(id), CONSTRAINT tin_dang_ban_cho_phuong_xa_id_fkey FOREIGN KEY (phuong_xa_id) REFERENCES public.phuong_xa(id), CONSTRAINT tin_dang_ban_cho_tin_dang_id_fkey FOREIGN KEY (tin_dang_id) REFERENCES public.tin_dang(id) ON DELETE CASCADE);


-- public.tin_dang_tien_ich definition

-- Drop table

-- DROP TABLE public.tin_dang_tien_ich;

CREATE TABLE public.tin_dang_tien_ich ( tin_dang_id int4 NOT NULL, tien_ich_id int4 NOT NULL, CONSTRAINT tin_dang_tien_ich_pkey PRIMARY KEY (tin_dang_id, tien_ich_id), CONSTRAINT tin_dang_tien_ich_tien_ich_id_fkey FOREIGN KEY (tien_ich_id) REFERENCES public.tien_ich(id), CONSTRAINT tin_dang_tien_ich_tin_dang_id_fkey FOREIGN KEY (tin_dang_id) REFERENCES public.tin_dang(id));


-- public.tin_yeu_thich definition

-- Drop table

-- DROP TABLE public.tin_yeu_thich;

CREATE TABLE public.tin_yeu_thich ( id serial4 NOT NULL, nguoi_dung_id int4 NOT NULL, tin_dang_id int4 NOT NULL, ngay_luu timestamptz DEFAULT now() NOT NULL, CONSTRAINT tin_yeu_thich_pkey PRIMARY KEY (id), CONSTRAINT uq_nguoi_dung_tin_dang_yeu_thich UNIQUE (nguoi_dung_id, tin_dang_id), CONSTRAINT tin_yeu_thich_nguoi_dung_id_fkey FOREIGN KEY (nguoi_dung_id) REFERENCES public.nguoi_dung(id), CONSTRAINT tin_yeu_thich_tin_dang_id_fkey FOREIGN KEY (tin_dang_id) REFERENCES public.tin_dang(id));


-- public.bao_cao definition

-- Drop table

-- DROP TABLE public.bao_cao;

CREATE TABLE public.bao_cao ( id serial4 NOT NULL, tin_dang_id int4 NOT NULL, nguoi_bao_cao_id int4 NOT NULL, ly_do varchar(150) NOT NULL, mo_ta text NULL, trang_thai varchar(20) NOT NULL, nguoi_xu_ly_id int4 NULL, ngay_bao_cao timestamptz DEFAULT now() NOT NULL, ngay_xu_ly timestamptz NULL, ghi_chu_xu_ly text NULL, CONSTRAINT bao_cao_pkey PRIMARY KEY (id), CONSTRAINT bao_cao_nguoi_bao_cao_id_fkey FOREIGN KEY (nguoi_bao_cao_id) REFERENCES public.nguoi_dung(id), CONSTRAINT bao_cao_nguoi_xu_ly_id_fkey FOREIGN KEY (nguoi_xu_ly_id) REFERENCES public.nguoi_dung(id), CONSTRAINT bao_cao_tin_dang_id_fkey FOREIGN KEY (tin_dang_id) REFERENCES public.tin_dang(id));


-- public.hinh_anh_tin_dang definition

-- Drop table

-- DROP TABLE public.hinh_anh_tin_dang;

CREATE TABLE public.hinh_anh_tin_dang ( id serial4 NOT NULL, tin_dang_id int4 NOT NULL, thu_tu_hien_thi int4 NOT NULL, la_anh_dai_dien bool NOT NULL, anh_thu_vien_id int4 NOT NULL, CONSTRAINT hinh_anh_tin_dang_pkey PRIMARY KEY (id), CONSTRAINT hinh_anh_tin_dang_anh_thu_vien_id_fkey FOREIGN KEY (anh_thu_vien_id) REFERENCES public.anh_thu_vien(id), CONSTRAINT hinh_anh_tin_dang_tin_dang_id_fkey FOREIGN KEY (tin_dang_id) REFERENCES public.tin_dang(id));