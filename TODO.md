# TODO - Session Persistence & Real-time Notifications

## ✅ Completed

## 📋 Pending Tasks

### 1. Session Persistence (Stay logged in on refresh)
- [ ] Improve session restoration mechanism to check session BEFORE showing login page
- [ ] Use query parameters or hidden input field more reliably
- [ ] Make session restoration happen automatically without user intervention

### 2. Real-time Notifications (No page refresh needed)
- [ ] Create a simple API endpoint for checking notifications without full page rerun
- [ ] Implement JavaScript polling that directly fetches notification data
- [ ] Show real-time toast/alert when admin assigns a task to agent
- [ ] Auto-refresh notification display without page reload

## Implementation Notes:
- Session persistence: Use st.query_params for reliable session restoration
- Real-time notifications: Use JavaScript fetch API to poll notifications.json directly

