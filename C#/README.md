## Introduction

+ Basic
    * .Net Core
    * Environment Settings
+ ASP MVC
    * MVC (Model View Controller) Framework
        - Model (Data Structure)
        - View (UI)
        - Controller (User Interaction)
        <p align="center">
          <img src="https://raw.githubusercontent.com/Draveness/analyze/master/contents/architecture/images/mvx/Standard-MVC.jpg" width="60%"/>
        </p>
        Why using it?: Can separate the operation, data presentation and logic control from each other
    * ASP (Active Server Pages) Url system
    * Razor
+ Entity Framework
    * Repository 
    * Code First
    * Mapping
    * CRUD
+ Identity
    * Authorization
    * Authentication

## Environments
When doing the development, developers usually separate the environment into: 
+ Development Env
+ Integration Env
+ Testing Env
+ Staging Env
+ Production Env

## Two Url Routing Mapping Patterns
+ Conventional routing
    * Url consists of "controller" and "action". e.g. {domain}/{controller}/{action}
    * using routing table to setup the rules of routing. e.g. using routes.MapRoute()
+ Attribute routing


