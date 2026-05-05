# TODO Steps Tracking for Hotel App Fixes - IMPLEMENTATION STARTED ✅

## Approved Plan Steps
1. ✅ **Create/Update TODO.md** - Done
2. 🔄 **Edit app.py** 
   - [ ] Remove duplicate get_tabs_for_role() definitions → **SINGLE CLEAN VERSION**
   - [ ] Fix get_tabs_for_role(): Ensure full 9-tab admin list
   - [ ] Fix tab unpacking in show_main_app(): Use dynamic tabs[i]
   - [ ] Import & call reservations_tab() confirmed OK → `from reservations_tab import reservations_tab`
3. ⏳ **Test** - Kill terminals + `python -m streamlit run app.py --server.port 8501 --logger.level error`
4. 🔍 **Verify** 
   - Admin: All 9 tabs, no unpacking error, Reservations (tab1) works
   - Receptionniste: 4 tabs, Reservations (tab1) CRUD
5. ⏳ **attempt_completion**

## Progress
- **Step 2**: Creating clean app.py now
- Current terminals (8503/8504): Kill before testing new version

