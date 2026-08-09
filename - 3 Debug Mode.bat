@echo off
:: Launch eraTW Debug Mode


START LazyLoadingV2.exe -debug
wmic process where name="LazyLoadingV2.exe" CALL setpriority 128