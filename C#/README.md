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
        __Why using it?:__ 
        + Can separate the operation (Model), data presentation (View) and logic control (Controller) from each other
        + Low coupling
        + High reusability
        + High maintainability  
        __Drawbacks:__
        + Hard to totally understand how it works
        + Structure is complex
        + Data flow is inefficient
    * ASP (Active Server Pages) Url system
    * Razor
+ Entity Framework
    * Repository 
    * Code First
    * Mapping
    * CRUD  
    __Highlights__:
    * Cross-platform
    * Modeling
    * CRUD (using Linq with sync/async)
    * Concurrence
    * Cache
    * Data Migration  
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

## Additional Concepts:
+ MVVM: Model - View - View Model
    Short explanation: View Model can manage multiple models



