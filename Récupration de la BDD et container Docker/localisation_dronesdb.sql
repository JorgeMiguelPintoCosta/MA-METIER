--
-- PostgreSQL database dump
--

\restrict zeRvhetqUarBcQt5gxvW7k5HRbIhGNJlWa5PKpmsUTgs9FBSIE6hJA6YZPDoIJd

-- Dumped from database version 14.20 (Debian 14.20-1.pgdg13+1)
-- Dumped by pg_dump version 14.20 (Debian 14.20-1.pgdg13+1)

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
-- Name: alerts; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.alerts (
    id integer NOT NULL,
    level text,
    message text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.alerts OWNER TO admin;

--
-- Name: alerts_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.alerts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.alerts_id_seq OWNER TO admin;

--
-- Name: alerts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.alerts_id_seq OWNED BY public.alerts.id;


--
-- Name: drones; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.drones (
    id integer NOT NULL,
    drone_type text,
    detected_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.drones OWNER TO admin;

--
-- Name: drones_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.drones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.drones_id_seq OWNER TO admin;

--
-- Name: drones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.drones_id_seq OWNED BY public.drones.id;


--
-- Name: signal_events; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.signal_events (
    id integer NOT NULL,
    signal_strength integer,
    approx_distance integer,
    relative_power real,
    bandwidth real,
    score integer,
    detection_time real
);


ALTER TABLE public.signal_events OWNER TO admin;

--
-- Name: signal_events_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.signal_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.signal_events_id_seq OWNER TO admin;

--
-- Name: signal_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.signal_events_id_seq OWNED BY public.signal_events.id;


--
-- Name: alerts id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.alerts ALTER COLUMN id SET DEFAULT nextval('public.alerts_id_seq'::regclass);


--
-- Name: drones id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.drones ALTER COLUMN id SET DEFAULT nextval('public.drones_id_seq'::regclass);


--
-- Name: signal_events id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.signal_events ALTER COLUMN id SET DEFAULT nextval('public.signal_events_id_seq'::regclass);


--
-- Data for Name: alerts; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.alerts (id, level, message, created_at) FROM stdin;
\.


--
-- Data for Name: drones; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.drones (id, drone_type, detected_at) FROM stdin;
\.


--
-- Data for Name: signal_events; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.signal_events (id, signal_strength, approx_distance, relative_power, bandwidth, score, detection_time) FROM stdin;
\.


--
-- Name: alerts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.alerts_id_seq', 1, false);


--
-- Name: drones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.drones_id_seq', 1, false);


--
-- Name: signal_events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.signal_events_id_seq', 1, false);


--
-- Name: alerts alerts_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_pkey PRIMARY KEY (id);


--
-- Name: drones drones_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.drones
    ADD CONSTRAINT drones_pkey PRIMARY KEY (id);


--
-- Name: signal_events signal_events_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.signal_events
    ADD CONSTRAINT signal_events_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict zeRvhetqUarBcQt5gxvW7k5HRbIhGNJlWa5PKpmsUTgs9FBSIE6hJA6YZPDoIJd

