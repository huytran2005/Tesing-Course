-- =========================
-- SCHEMA ONLY (SAFE VERSION)
-- =========================

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

-- Fix UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================
-- TABLES
-- =========================

CREATE TABLE IF NOT EXISTS public.app_user (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    restaurant_id uuid,
    email varchar NOT NULL UNIQUE,
    password_hash varchar NOT NULL,
    display_name varchar,
    phone varchar,
    role varchar NOT NULL,
    created_at timestamptz DEFAULT now(),
    fcm_token text
);

CREATE TABLE IF NOT EXISTS public.restaurants (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name varchar(255) NOT NULL,
    description varchar,
    owner_id uuid NOT NULL,
    image_preview varchar,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.restaurant_table (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    restaurant_id uuid NOT NULL,
    name text NOT NULL,
    seats integer NOT NULL,
    status text,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.menu_category (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    restaurant_id uuid NOT NULL,
    name varchar NOT NULL,
    icon varchar
);

CREATE TABLE IF NOT EXISTS public.menu_item (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    restaurant_id uuid NOT NULL,
    category_id uuid NOT NULL,
    name varchar NOT NULL,
    description varchar,
    price numeric NOT NULL,
    is_available boolean DEFAULT true,
    image_url varchar,
    meta jsonb
);

CREATE TABLE IF NOT EXISTS public.orders (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    restaurant_id uuid NOT NULL,
    table_id uuid NOT NULL,
    qr_id uuid NOT NULL,
    user_id uuid,
    status varchar,
    total_amount numeric,
    currency varchar,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.order_line (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id uuid NOT NULL,
    menu_item_id uuid NOT NULL,
    item_name text NOT NULL,
    qty integer NOT NULL,
    unit_price numeric NOT NULL,
    note text,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.menu_item_review (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    restaurant_id uuid NOT NULL,
    order_id uuid NOT NULL,
    order_line_id uuid NOT NULL UNIQUE,
    menu_item_id uuid NOT NULL,
    rating integer NOT NULL,
    comment text,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.qr_code (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    restaurant_id uuid NOT NULL,
    table_id uuid NOT NULL,
    code varchar NOT NULL UNIQUE,
    type varchar,
    status varchar,
    image_path varchar,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.guest_session (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    qr_id uuid NOT NULL,
    session_token varchar NOT NULL UNIQUE,
    expires_at timestamptz NOT NULL,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.point_transaction (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id uuid NOT NULL,
    order_id uuid,
    points integer NOT NULL,
    reason varchar NOT NULL,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.user_point (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id uuid NOT NULL UNIQUE,
    total_points integer DEFAULT 0,
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.order_status_history (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id uuid,
    old_status varchar,
    new_status varchar,
    changed_by uuid,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.tenant (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name varchar(255) NOT NULL
);