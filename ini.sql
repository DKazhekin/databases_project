--
-- PostgreSQL database dump
--

-- Dumped from database version 16rc1
-- Dumped by pg_dump version 16rc1

-- Started on 2023-11-29 23:27:14 MSK

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2 (class 3079 OID 16384)
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- TOC entry 3670 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 230 (class 1259 OID 17231)
-- Name: cart; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cart (
    id integer NOT NULL,
    user_id integer NOT NULL,
    item_name character varying(50) NOT NULL,
    item_count integer NOT NULL
);


ALTER TABLE public.cart OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 17230)
-- Name: cart_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cart_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cart_id_seq OWNER TO postgres;

--
-- TOC entry 3671 (class 0 OID 0)
-- Dependencies: 229
-- Name: cart_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cart_id_seq OWNED BY public.cart.id;


--
-- TOC entry 226 (class 1259 OID 17186)
-- Name: courier_actions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.courier_actions (
    courier_action_id integer NOT NULL,
    courier_id integer,
    order_id integer,
    action character varying(20),
    "time" timestamp without time zone
);


ALTER TABLE public.courier_actions OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 17185)
-- Name: courier_actions_courier_action_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.courier_actions_courier_action_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.courier_actions_courier_action_id_seq OWNER TO postgres;

--
-- TOC entry 3672 (class 0 OID 0)
-- Dependencies: 225
-- Name: courier_actions_courier_action_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.courier_actions_courier_action_id_seq OWNED BY public.courier_actions.courier_action_id;


--
-- TOC entry 221 (class 1259 OID 17157)
-- Name: couriers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.couriers (
    courier_id integer NOT NULL,
    name character varying(20),
    birth_date date,
    sex character varying(10),
    phone_number character varying(20)
);


ALTER TABLE public.couriers OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 17156)
-- Name: couriers_courier_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.couriers_courier_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.couriers_courier_id_seq OWNER TO postgres;

--
-- TOC entry 3673 (class 0 OID 0)
-- Dependencies: 220
-- Name: couriers_courier_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.couriers_courier_id_seq OWNED BY public.couriers.courier_id;


--
-- TOC entry 224 (class 1259 OID 17169)
-- Name: order_body; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_body (
    order_body_id integer NOT NULL,
    order_id integer,
    product_id integer,
    counts integer
);


ALTER TABLE public.order_body OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 17168)
-- Name: order_body_order_body_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_body_order_body_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_body_order_body_id_seq OWNER TO postgres;

--
-- TOC entry 3674 (class 0 OID 0)
-- Dependencies: 223
-- Name: order_body_order_body_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_body_order_body_id_seq OWNED BY public.order_body.order_body_id;


--
-- TOC entry 217 (class 1259 OID 17143)
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    order_id integer NOT NULL,
    creation_time timestamp without time zone
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 17142)
-- Name: orders_order_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_order_id_seq OWNER TO postgres;

--
-- TOC entry 3675 (class 0 OID 0)
-- Dependencies: 216
-- Name: orders_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_order_id_seq OWNED BY public.orders.order_id;


--
-- TOC entry 219 (class 1259 OID 17150)
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    product_id integer NOT NULL,
    name character varying(50),
    price real,
    country character varying(50),
    url character varying(1024)
);


ALTER TABLE public.products OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 17149)
-- Name: products_product_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.products_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_product_id_seq OWNER TO postgres;

--
-- TOC entry 3676 (class 0 OID 0)
-- Dependencies: 218
-- Name: products_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.products_product_id_seq OWNED BY public.products.product_id;


--
-- TOC entry 228 (class 1259 OID 17203)
-- Name: user_actions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_actions (
    user_action_id integer NOT NULL,
    user_id integer,
    order_id integer,
    action character varying(20),
    "time" timestamp without time zone
);


ALTER TABLE public.user_actions OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 17202)
-- Name: user_actions_user_action_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_actions_user_action_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_actions_user_action_id_seq OWNER TO postgres;

--
-- TOC entry 3677 (class 0 OID 0)
-- Dependencies: 227
-- Name: user_actions_user_action_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_actions_user_action_id_seq OWNED BY public.user_actions.user_action_id;


--
-- TOC entry 222 (class 1259 OID 17163)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(20),
    balance integer
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 3484 (class 2604 OID 17234)
-- Name: cart id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart ALTER COLUMN id SET DEFAULT nextval('public.cart_id_seq'::regclass);


--
-- TOC entry 3482 (class 2604 OID 17189)
-- Name: courier_actions courier_action_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.courier_actions ALTER COLUMN courier_action_id SET DEFAULT nextval('public.courier_actions_courier_action_id_seq'::regclass);


--
-- TOC entry 3480 (class 2604 OID 17160)
-- Name: couriers courier_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.couriers ALTER COLUMN courier_id SET DEFAULT nextval('public.couriers_courier_id_seq'::regclass);


--
-- TOC entry 3481 (class 2604 OID 17172)
-- Name: order_body order_body_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_body ALTER COLUMN order_body_id SET DEFAULT nextval('public.order_body_order_body_id_seq'::regclass);


--
-- TOC entry 3478 (class 2604 OID 17146)
-- Name: orders order_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN order_id SET DEFAULT nextval('public.orders_order_id_seq'::regclass);


--
-- TOC entry 3479 (class 2604 OID 17153)
-- Name: products product_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products ALTER COLUMN product_id SET DEFAULT nextval('public.products_product_id_seq'::regclass);


--
-- TOC entry 3483 (class 2604 OID 17206)
-- Name: user_actions user_action_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_actions ALTER COLUMN user_action_id SET DEFAULT nextval('public.user_actions_user_action_id_seq'::regclass);


-- Completed on 2023-11-29 23:27:14 MSK
INSERT INTO public.products(name, price, country, url)
VALUES
	('Air Force 1',	149.99, 'China', 'https://cdn1.ozone.ru/s3/multimedia-e/6486597578.jpg'),
	('Air Jordan 1 Mid', 259.99, 'Thailand', 'https://www.newjordans2022.com/wp-content/uploads/2019/03/Air-Jordan-1-Mid-Chicago-White-Red-Black-For-Sale-6.jpg'),
    ('Supreme White T',	200, 'Netherlands', 'https://cdna.lystit.com/photos/stadiumgoods/c317143d/supreme-White-Paris-Box-Logo-Tee.jpeg'),
    ('Adidas x Bape Superstar',	200.99,	'China', 'https://godmeetsfashion.com/wp-content/uploads/2021/04/bape-a-bathing-ape-adidas-superstar-80s-abc-camo-gz8981-release-20210508-20.jpg'),
    ('Bape Zip Hoodie',	159.99,	'China', 'https://i.ebayimg.com/00/s/MTAwMFgxNDAw/z/wEcAAOSwik9bfwIw/$_57.JPG?set_id=8800005007'),
    ('Dickies Loose Jeans',	139.99,	'Saint-P', 'https://www.venuestore.com.au/media/catalog/product/cache/1/image/2000x/9df78eab33525d08d6e5fb8d27136e95/d/i/dickies_1994_relaxed_straight_fit_carpenter_denim_jeans_-_indigo_4.jpg'),
    ('Thrasher White T', 100, 'China',	'https://prokedi.ru/content/img/45/futbolka-thrasher-skate-goat-white_2982301.jpg'),
    ('Stone Island Balaclava', 259.99,	'Thaivan', 'https://images.are.na/eyJidWNrZXQiOiJhcmVuYV9pbWFnZXMiLCJrZXkiOiIzNjg4NzgzL29yaWdpbmFsX2VlYzE2NzliNjUyYmQwZGZjZTIwZDZiYmU1NTA3NTViLmpwZyIsImVkaXRzIjp7InJlc2l6ZSI6eyJ3aWR0aCI6MTIwMCwiaGVpZ2h0IjoxMjAwLCJmaXQiOiJpbnNpZGUiLCJ3aXRob3V0RW5sYXJnZW1lbnQiOnRydWV9LCJ3ZWJwIjp7InF1YWxpdHkiOjkwfSwianBlZyI6eyJxdWFsaXR5Ijo5MH0sInJvdGF0ZSI6bnVsbH19?bc=1')
--
-- PostgreSQL database dump complete
--