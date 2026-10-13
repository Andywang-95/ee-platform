-- Development only. Creates the two databases the platform expects on one
-- SQL Server, and the parts table that exists already at the company.
-- Safe to run repeatedly.
--
-- The parts table columns are assumptions; see
-- docs/domains/parts-schema-assumptions.md.

IF DB_ID('ee_platform') IS NULL CREATE DATABASE ee_platform;
IF DB_ID('ee_parts') IS NULL CREATE DATABASE ee_parts;
GO

USE ee_parts;
GO

IF OBJECT_ID('dbo.parts') IS NULL
CREATE TABLE dbo.parts (
    id INT NOT NULL PRIMARY KEY,
    part_number NVARCHAR(50) NOT NULL,
    table_name NVARCHAR(20) NOT NULL,
    description NVARCHAR(255) NULL,
    value NVARCHAR(50) NULL,
    tolerance NVARCHAR(20) NULL,
    power_rating NVARCHAR(20) NULL,
    voltage_rating NVARCHAR(20) NULL,
    current_rating NVARCHAR(20) NULL,
    package NVARCHAR(50) NULL,
    manufacturer NVARCHAR(100) NULL,
    manufacturer_part_number NVARCHAR(100) NULL,
    schematic_part NVARCHAR(255) NULL,
    pcb_footprint NVARCHAR(255) NULL,
    remark NVARCHAR(MAX) NULL
);
GO
