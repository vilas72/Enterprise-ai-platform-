# Demo Scenarios

This document outlines seven demonstration scenarios that showcase the platform's capabilities to different stakeholder groups.

## 1. Developer Assistant

**Target Audience**: Engineering Leaders, CTO

**Scenario**: Developer uses the platform to understand codebase and solve coding problems.

### Setup
- Index: Company codebase (Python, TypeScript, documentation)
- Context: Git history, architecture docs, API documentation
- Knowledge Base: Best practices, coding standards, performance guidelines

### Demo Flow
```
1. Developer asks: "How do I implement pagination in the user service?"
   
   Platform:
   - Retrieves: UserService code, pagination utilities, API patterns
   - Rewrites: "Show pagination patterns for REST APIs in user service"
   - Responds: Provides code example with explanation
   
2. Developer: "Why does this take 5 seconds?"
   
   Platform:
   - Maintains context of previous service
   - Retrieves: Database queries, N+1 patterns, performance docs
   - Responds: Identifies N+1 query problem, suggests fix
   
3. Developer: "What's our standard for logging?"
   
   Platform:
   - Retrieves: Logging standards doc, examples from codebase
   - Responds: Provides logging patterns and why they matter
```

### Value Prop
- ✅ Onboard developers 50% faster
- ✅ Reduce knowledge silos
- ✅ Consistent code quality

**KPIs**: Average onboarding time, code review cycle time

---

## 2. Knowledge Assistant

**Target Audience**: Knowledge Workers, HR, Operations

**Scenario**: Employees access company knowledge base through conversational interface.

### Setup
- Index: Company wiki, employee handbook, policies, procedures
- Context: Employee profile, department, role
- Knowledge Base: Benefits, travel policies, HR procedures

### Demo Flow
```
1. Employee: "How much PTO do I have this year?"
   
   Platform:
   - Understands: Employee context (level, department, location)
   - Retrieves: PTO policy, employee record insights
   - Responds: "As a Senior Engineer in US, you have 20 days"
   
2. Employee: "What's the travel approval process?"
   
   Platform:
   - Retrieves: Travel policy, approval workflows, cost thresholds
   - Responds: Step-by-step process with approver info
   
3. Employee: "Can I work from Barcelona for 2 weeks?"
   
   Platform:
   - Retrieves: Remote policy, visa requirements, tax implications
   - Responds: Yes with process steps and tax considerations
```

### Value Prop
- ✅ Reduce HR support tickets by 40%
- ✅ 24/7 policy assistance
- ✅ Consistent policy interpretation

**KPIs**: HR ticket reduction, response time, employee satisfaction

---

## 3. Jira Assistant

**Target Audience**: Product Managers, Engineering Managers

**Scenario**: Quick Q&A about project status, ticket details, and sprint planning.

### Setup
- Index: Jira issues, project docs, requirements
- Context: Current sprint, team capacity, project roadmap
- Knowledge Base: Project history, decisions, blockers

### Demo Flow
```
1. Manager: "What's blocking our authentication feature?"
   
   Platform:
   - Retrieves: Auth feature epic, related issues, comments
   - Identifies: "Waiting on security team review (4 days)"
   - Responds: With status, owner, next steps
   
2. Manager: "Can we fit this in the next sprint?"
   
   Platform:
   - Considers: Sprint capacity, dependencies, current load
   - Responds: "Yes, if we defer search optimization by 1 week"
   
3. Manager: "What did we decide about API versioning?"
   
   Platform:
   - Retrieves: Relevant ADRs, discussions, decisions
   - Responds: With context and implementation guidance
```

### Value Prop
- ✅ Real-time project visibility
- ✅ Reduce status meeting time
- ✅ Data-driven sprint planning

**KPIs**: Meeting time reduction, sprint predictability

---

## 4. GitHub Assistant

**Target Audience**: Technical Leadership, Security Team

**Scenario**: Code review assistant that understands PRs, dependencies, and security implications.

### Setup
- Index: GitHub repositories, PRs, issues, security policies
- Context: PR diff, dependencies, security guidelines
- Knowledge Base: Approved libraries, security patterns, anti-patterns

### Demo Flow
```
1. Reviewer: "Is this third-party library safe to use?"
   
   Platform:
   - Checks: CVE database, community reviews, license compatibility
   - Responds: "Yes, with 2 open issues (low severity)"
   
2. Reviewer: "This PR adds 100KB - is that acceptable?"
   
   Platform:
   - Understands: Bundle size targets, library justification
   - Responds: "Exceeds limit by 20%. Suggest tree-shaking or lazy load"
   
3. Reviewer: "Any security concerns here?"
   
   Platform:
   - Identifies: SQL potential, auth patterns, data exposure
   - Responds: "Parameterized queries used correctly. Consider rate limiting"
```

### Value Prop
- ✅ Faster code reviews (40% time savings)
- ✅ Consistent security standards
- ✅ Better dependency management

**KPIs**: PR review time, security incident reduction

---

## 5. SQL Assistant

**Target Audience**: Data Analysts, Business Intelligence

**Scenario**: Natural language to SQL with understanding of data model and business logic.

### Setup
- Index: Database schema, table documentation, BI queries
- Context: Data dictionary, business logic, performance patterns
- Knowledge Base: Common aggregations, date handling, business rules

### Demo Flow
```
1. Analyst: "Give me monthly revenue for Q4"
   
   Platform:
   - Understands: Revenue definition, billing cycles, date logic
   - Generates: Optimized SQL with proper joins and aggregations
   - Explains: Query logic and data freshness
   
2. Analyst: "How does this compare to last year?"
   
   Platform:
   - Remembers context (Q4 revenue)
   - Generates: YoY comparison with proper date handling
   - Responds: With trends and anomalies
   
3. Analyst: "Is there an index for this query?"
   
   Platform:
   - Analyzes: Query plan, available indexes
   - Responds: With performance insights and optimization suggestions
```

### Value Prop
- ✅ 10x faster ad-hoc query creation
- ✅ Consistent SQL style and performance
- ✅ Knowledge preservation for team

**KPIs**: Query creation time, data accuracy, query performance

---

## 6. Incident Response Assistant

**Target Audience**: SREs, DevOps, On-Call Engineers

**Scenario**: Quick guidance during incidents with access to runbooks and historical context.

### Setup
- Index: Runbooks, incident history, alerts, documentation
- Context: Current alerts, recent changes, team expertise
- Knowledge Base: Troubleshooting guides, known issues, escalation paths

### Demo Flow
```
1. On-Call: "Database replication is lagging"
   
   Platform:
   - Retrieves: DB replication runbook, similar past incidents
   - Responds: Step-by-step diagnostics and fixes
   
2. On-Call: "Tried the standard steps, still broken"
   
   Platform:
   - Recalls: Previous conversation context
   - Retrieves: Advanced troubleshooting, escalation procedures
   - Responds: Who to page, what info to gather
   
3. On-Call: "We're seeing this for the 3rd time"
   
   Platform:
   - Identifies: Recurring issue pattern
   - Suggests: Root cause investigation, permanent fix options
   - Responds: With business impact and fix complexity
```

### Value Prop
- ✅ Reduce MTTR by 30-50%
- ✅ Improve first-contact resolution
- ✅ Preserve incident knowledge

**KPIs**: MTTR (Mean Time To Resolution), incident severity, team confidence

---

## 7. Document Q&A

**Target Audience**: Legal, Compliance, Sales

**Scenario**: Ask questions about large document sets (contracts, regulations, product docs).

### Setup
- Index: PDFs, Word docs, regulatory documents, RFP responses
- Context: Document type, date, regulatory framework
- Knowledge Base: Legal templates, compliance checklists, standard clauses

### Demo Flow
```
1. Sales: "What's our warranty in this contract?"
   
   Platform:
   - Retrieves: Warranty sections from contract
   - Extracts: Key terms, limitations, durations
   - Responds: "90 days on defects, excludes misuse"
   
2. Compliance: "Are we GDPR compliant for this solution?"
   
   Platform:
   - Retrieves: GDPR requirements, product architecture, data flow
   - Analyzes: Data residence, consent mechanisms, retention
   - Responds: "Yes, with these safeguards in place"
   
3. Legal: "How does this contract compare to our template?"
   
   Platform:
   - Compares: Deviation analysis, risk assessment
   - Responds: "3 major deviations in liability and IP terms"
```

### Value Prop
- ✅ Instant document insights (vs. manual review)
- ✅ Reduce legal review cycles
- ✅ Better compliance risk management

**KPIs**: Document review time, compliance risk score, contract velocity

---

## Demo Delivery Strategy

### For Each Demo

1. **Setup Phase** (2 min)
   - Show indexed knowledge base
   - Explain context & personalization

2. **Interactive Phase** (5-7 min)
   - Show 3 conversation turns (not just single Q&A)
   - Demonstrate context understanding
   - Show memory/summarization capabilities

3. **Explanation Phase** (3 min)
   - Show actual RAG pipeline (retrieval, reranking)
   - Highlight key differentiators
   - Map to customer's use case

4. **Business Impact** (2 min)
   - Show metrics from similar customers
   - ROI calculation
   - Implementation timeline

### Recommended Audience Mapping

| Demo | Best For | Decision Maker |
|------|----------|--------|
| Developer Assistant | Tech companies, Startups | VP Engineering |
| Knowledge Assistant | Enterprise, HR-heavy orgs | CHRO, COO |
| Jira Assistant | Tech companies | VP Product |
| GitHub Assistant | Open Source, DevTools | CISO, VP Eng |
| SQL Assistant | Data-driven orgs | VP Analytics, CFO |
| Incident Response | Infrastructure heavy | VP Operations, CISO |
| Document Q&A | Legal, Compliance, Finance | CLO, CFO |
