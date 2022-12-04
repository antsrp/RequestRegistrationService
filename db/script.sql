CREATE TABLE IF NOT EXISTS public.appeals(
    id SERIAL PRIMARY KEY,
    surname character varying(50) NOT NULL,
    name character varying(50) NOT NULL,
    patronymic character varying(50) NOT NULL,
    phone text NOT NULL,
    appeal_text text NOT NULL
);
