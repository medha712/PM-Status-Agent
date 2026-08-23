# 📊 Sample Weekly Project Status Report
**Generated:** 2026-08-23 14:30:00

## Health Overview
- **Overall Health:** 72% (⚠️ at_risk) 📈 improving
- **Completed Items:** 37/51
- **Total Blockers:** 5

---

## Platform Progress

### Jira Sprint (PROJ Sprint 42)
- **Completion:** 66.7% (16/24 done)
- **In Progress:** 5 issues
- **To Do:** 3 issues
- **Status:** At Risk
- **Sprint Duration:** Aug 16 - Aug 30

### Asana Projects
- **Completion:** 65.6% (21/32 completed)
- **At Risk:** 4 tasks
- **Overall Status:** On Track
- **Progress:** 65% toward deadline

### Notion Initiatives
- **Total Initiatives:** 4
- **In Progress:** 2
- **Completed:** 1
- **Blocked:** 1

---

## 🚨 Blockers (5 total)

**Current blocker count is STABLE** - approximately the same as last week

### Top Blockers:

**1. Set up payment webhooks** (Jira: PROJ-105)
   - Type: Stuck in progress
   - Days Blocked: 7
   - Priority: High
   - Assignee: eve@company.com
   - **Action:** Check if awaiting external API documentation

**2. Database optimization** (Asana: task-202)
   - Type: Overdue
   - Days Overdue: 2
   - Priority: High
   - Assignee: grace@company.com
   - **Action:** Requires immediate attention

**3. Customer feedback integration** (Notion: n2)
   - Type: External blocker
   - Status: Blocked
   - Priority: P1
   - Owner: jack@company.com
   - Reason: Waiting on external API documentation from vendor

**4. Implement Stripe payment integration** (Jira: PROJ-102)
   - Type: Dependency blocked
   - Blocked by: PROJ-105
   - Days Blocked: 5
   - Priority: Critical
   - Assignee: bob@company.com
   - **Impact:** Critical path - unblock PROJ-105 to proceed

**5. Security audit compliance** (Asana: task-203)
   - Type: At risk
   - Status: On Hold
   - Assignee: henry@company.com
   - **Note:** Scheduled for unblock on 2026-08-28

---

## ⚠️ Chronic Issues (Items stuck 2+ weeks)

**Critical Finding:** 1 item stuck for multiple weeks

**Set up payment webhooks** (Jira: PROJ-105)
- **Source:** Jira
- **Type:** Stuck in progress
- **Weeks Stuck:** 2 weeks
- **First Seen:** 2026-W33
- **Timeline:** 2026-W33 → 2026-W34
- **Assignee:** eve@company.com
- **Recommended Action:** 
  - Schedule sync with eve
  - Identify blocking dependencies
  - Allocate additional resources if needed
  - Consider breaking into smaller tasks

---

## 🚩 Risk Flags

### 🔴 CRITICAL RISKS: None
Current health is not critical, but approaching at-risk threshold

### 🟡 MEDIUM RISKS:

1. **Blocker Trend:** STABLE
   - Current: 5 blockers
   - Average: 4.2 over past 4 weeks
   - No significant increase, but elevated

2. **Payment Work Dependency Chain**
   - PROJ-102 (Stripe integration) blocked by PROJ-105
   - PROJ-105 stuck for 7 days
   - **Risk:** Critical path delay if not resolved by end of sprint

3. **Overdue Asana Task**
   - task-202 (Database optimization) 2 days overdue
   - **Risk:** May impact performance targets

### 📊 Team Capacity Risk
- 5 items in progress concurrently (normal for team of 5)
- High-priority items somewhat distributed
- Eve appears overloaded (PROJ-105 stuck)

---

## 📈 Week-over-Week Trends

### Health Score Trend
```
2026-W32: [████████░░] 80.0%
2026-W33: [██████░░░░] 60.0%  ↓ -20%
2026-W34: [███████░░░] 70.0%  ↑ +10% (recovering)
2026-W35: [████████░░] 72.0%  ↑ +2%  (trend: improving)
```
**Analysis:** Recovery trend is positive. Health declining in W33 due to PROJ-105 blockers, now improving.

### Blocker Count Trend
```
2026-W32: 3 blockers
2026-W33: 5 blockers  ↑ +2
2026-W34: 5 blockers  ➡️  stable
2026-W35: 5 blockers  ➡️  stable
```
**Analysis:** Introduced 2 new blockers in W33. Not resolving at expected rate.

### Completion Velocity
```
2026-W32: 12 items completed
2026-W33:  8 items completed  ↓ -4
2026-W34: 10 items completed  ↑ +2
2026-W35: 11 items completed  ↑ +1
```
**Analysis:** Velocity dipped in W33 due to blockers, recovering well now.

---

## 💡 Recommendations

### Immediate Actions (This Week)
1. **Unblock Payment Work**
   - Schedule sync with eve@company.com TODAY
   - Define blockers on PROJ-105 (payment webhooks)
   - If external API docs pending, contact vendor by EOD Thursday

2. **Handle Overdue Task**
   - grace@company.com: Update status on task-202 (Database optimization)
   - If blocked, escalate; if just delayed, confirm new completion date

### Short-term Actions (Next Week)
3. **Resolve Chronic Blocker**
   - PROJ-105 has been stuck for 2 weeks
   - Plan intensive work session or pair programming
   - Consider breaking into smaller, deliverable pieces

4. **Improve Trend**
   - Monitor health score - still below 75% threshold
   - Target getting to 80%+ by end of sprint
   - Reduce blocker count from 5 → 3 this week

### Process Improvements
5. **Dependency Visibility**
   - Payment work has cross-team dependency
   - Ensure PROJ-105 resolution is on critical path board
   - Daily standup check-in on blocking status

6. **Blocker Prevention**
   - Current blockers mostly externally driven (vendor API, cross-team)
   - Implement earlier vendor engagement for future integrations

---

## 📋 Summary for Leadership

| Metric | Current | 4-Week Avg | Status | Trend |
|--------|---------|-----------|--------|-------|
| Health Score | 72% | 70% | At Risk | 📈 Improving |
| Blockers | 5 | 4.2 | Elevated | ➡️ Stable |
| Velocity | 11 items | 10.25 | Good | 📈 Improving |
| Completion Rate | 72.5% | 70% | Good | ✅ On Track |

**Bottom Line:** Project recovering from W33 dip. Key payment work blocker needs urgent attention. Expected to return to healthy status by end of sprint if PROJ-105 resolved by Thursday.

---

## Questions the Agent Can Answer

Ask the agent:
- "What's been stuck for more than one sprint?" → Identify chronic blockers
- "What are the critical risks?" → Get risk assessment view
- "How's our velocity trending?" → Velocity analysis
- "What's blocking payment work?" → Dependency analysis
- "Show me items overdue by team member" → Team performance view
- "What should we fix first?" → Priority recommendations

---

**Next Report:** 2026-08-30 (Following Friday)
**Questions?** Run the agent with specific queries or request custom analysis
