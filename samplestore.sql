--
-- PostgreSQL database dump
--

-- Dumped from database version 12.9 (Ubuntu 12.9-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.9 (Ubuntu 12.9-0ubuntu0.20.04.1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    ext_id text NOT NULL,
    order_value text NOT NULL,
    order_items jsonb,
    date text NOT NULL,
    user_id text NOT NULL
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_id_seq OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: store; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.store (
    item_id integer NOT NULL,
    item_name text NOT NULL,
    item_price text NOT NULL,
    item_image text
);


ALTER TABLE public.store OWNER TO postgres;

--
-- Name: store_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.store_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.store_item_id_seq OWNER TO postgres;

--
-- Name: store_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.store_item_id_seq OWNED BY public.store.item_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username text NOT NULL,
    password text NOT NULL,
    address text
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: wishlist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wishlist (
    user_id integer,
    wishlist jsonb
);


ALTER TABLE public.wishlist OWNER TO postgres;

--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: store item_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store ALTER COLUMN item_id SET DEFAULT nextval('public.store_item_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, ext_id, order_value, order_items, date, user_id) FROM stdin;
1	2021-12-31/96443	25	["Men's White T-shirt"]	2021-12-31 19:53:27.065017	1
2	2021-12-31/66022	30	["Women's Black T-shirt"]	2021-12-31 19:56:20.977406	1
3	2021-12-31/19680	60	["Women's Pink Blazer", "Women's Yellow T-shirt"]	2021-12-31 21:08:13.563626	5
4	2021-12-31/78725	25	["Men's Yellow T-shirt"]	2021-12-31 23:10:51.143791	1
5	2021-12-31/51763	28.5	["Women's Pink Blazer"]	2021-12-31 23:15:38.034549	1
\.


--
-- Data for Name: store; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.store (item_id, item_name, item_price, item_image) FROM stdin;
1	Men's White T-shirt	20	whitetee.jpg
2	Men's Black T-shirt	25	blacktee.jpg
3	Men's Yellow T-shirt	20	yellowtee.jpg
4	Men's Red T-shirt	15	redtee.jpg
5	Men's Purple T-shirt	15	purpletee.jpg
6	Women's Black T-shirt	30	womenteeblack.jpeg
7	Women's Yellow T-shirt	30	womenteeyellow.jpeg
8	Women's Green T-shirt	30	womenteegreen.jpg
9	Women's Pink Blazer	30	womenblazerpink.jpg
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password, address) FROM stdin;
2	aayush	pbkdf2:sha256:150000$Bp0MCiUg$dc112fe2ae42368ea69b62702d3d684f41b1e7d5286d5ff328d644533a64ac56	H.No. 123, Sector - 5, Najafgarh, New Delhi 110051
3	Manoj	pbkdf2:sha256:150000$I8vPF7Fd$8c7a33a44164f5c05356ed1fb99057a35656bb0c94b3b40c7196447109907554	H.No. 12, Sector - 5, Rohtak
4	Renu	pbkdf2:sha256:150000$fhNJD4SY$404a4b4cc9fa0531be21a4a970befa5d77a23d28a5fde62a7ccffa1bf4af61ff	T02-204, Sare Crescent Parc, Sec - 92, Gurgaon, 122505
1	Deepank	pbkdf2:sha256:150000$4QvJt7t9$d9f4c5481b1539a6ebeca7d164245d6e0f0280c92e20edeaa5a6f2e455191a92	711-2880 Nulla St.\r\nMankato Mississippi 96522\r\n(257) 563-7401
5	renu	pbkdf2:sha256:150000$oNZs0GI6$2233c5a30cd9d179c7bbc8d03cd16563bb1efcdc44790966252cd82ed4d311a6	1125, Sector - 23, Mumbai
\.


--
-- Data for Name: wishlist; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wishlist (user_id, wishlist) FROM stdin;
\.


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 5, true);


--
-- Name: store_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.store_item_id_seq', 9, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 5, true);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: store store_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store
    ADD CONSTRAINT store_pkey PRIMARY KEY (item_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

