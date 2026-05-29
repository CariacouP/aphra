## 2024-03-XX - [Combine Multi-Sector Ticker Fetching into a Single Request]
**Learning:** `signal_generator.py` iterates over sectors and runs `loader.fetch_batch(tickers)` for each sector sequentially. For a backtest scanning the whole market, we are doing separate `yf.download` API calls per sector, adding overhead and taking longer. YFinance processes large batches significantly faster than multiple smaller batches.
**Action:** Extract all tickers across all sectors, call `fetch_batch` once, and then map the data back to their respective sectors.

## 2026-03-11 - [Lazy Load Heavy Modules in Flask App]
**Learning:** `webapp/app.py` imported `pandas`, `src.data_manager`, and `src.backtester` at the module level. These heavy libraries were delaying the Flask web server startup and increasing initial load time, despite not being needed for every route.
**Action:** Move heavy imports like `import pandas as pd` and `from src.backtester import run_backtest` inside the functions that actually require them (e.g., `build_kpi_table` and `execute_backtest`). This improved Flask import time from ~3.5s to ~0.25s.

## 2026-03-14 - [Optimize Pandas Index Filtering]
**Learning:** In `src/backtester.py`, slicing data frames up to a current date for every ticker across every backtest day using boolean arrays (e.g., `df[df.index <= current_date]`) is O(N) and creates unnecessary object copies inside a hot loop, causing massive performance drops.
**Action:** Utilize `df.index.searchsorted(current_date, side="right")` on datetime indices, which executes an O(log N) binary search, then retrieve the data via `.iloc[:idx].copy()`. This drops the time cost of generating daily slices by roughly 70-80%.
## 2024-05-18 - [Optimize Pandas Max and Series Operations]
**Learning:** `pd.concat([series1, series2, series3], axis=1).max(axis=1)` is computationally expensive for technical indicators like ATR compared to nested `np.maximum()` operations. Additionally, constructing a `pd.Series` from a NumPy array without explicitly providing `index=df.index` leads to costly re-alignment overhead in rolling calculations.
**Action:** Replace `pd.concat(...).max(axis=1)` with nested element-wise `np.maximum()` operations. Explicitly provide the target index (e.g., `pd.Series(arr, index=df.index)`) when constructing a series for operations like `.rolling()`.

## 2026-05-17 - Migration de l'architecture Backend vers Celery/Redis
**Problème :** L'application web utilisait des  locaux et des dictionnaires globaux en mémoire pour le cache et l'exécution asynchrone des backtests. En production avec Gunicorn, cette approche entraine un gaspillage de ressources, des pertes d'état inter-processus et potentiellement l'apparition de processus orphelins.
**Solution :** Migration de la gestion de l'état asynchrone vers un courtier de messages dédié (Redis) et une file de traitement (Celery). Une gestion fine des exceptions garantit également un "fallback" vers l'ancien système (in-memory) si Redis est momentanément inaccessible, afin de ne pas briser les environnements locaux sans Docker.
**Apprentissage :** Toujours vérifier les cibles de "mock" dans les tests unitaires. Le remplacement du routeur d'exécution par  nécessite de mocker le wrapper final (ex: ) et non l'exécuteur bas-niveau  qui n'est plus appelé.

## 2024-05-16 - Migration de l'architecture Backend vers Celery/Redis
**Problème :** L'application web utilisait des `ProcessPoolExecutor` locaux et des dictionnaires globaux en mémoire pour le cache et l'exécution asynchrone des backtests. En production avec Gunicorn, cette approche entraine un gaspillage de ressources, des pertes d'état inter-processus et potentiellement l'apparition de processus orphelins.
**Solution :** Migration de la gestion de l'état asynchrone vers un courtier de messages dédié (Redis) et une file de traitement (Celery). Une gestion fine des exceptions garantit également un "fallback" vers l'ancien système (in-memory) si Redis est momentanément inaccessible, afin de ne pas briser les environnements locaux sans Docker.
**Apprentissage :** Toujours vérifier les cibles de "mock" dans les tests unitaires. Le remplacement du routeur d'exécution par `Celery.delay()` nécessite de mocker le wrapper final (ex: `submit_grid_search`) et non l'exécuteur bas-niveau `get_process_executor` qui n'est plus appelé.
