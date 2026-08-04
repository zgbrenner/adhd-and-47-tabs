# Interaction patterns

Use this reference when a task needs state, recovery, or adaptation beyond the four base contracts. Do not expose every label mechanically.

## 1. Router

Choose the base contract first:

| User need | Base contract | First visible content |
|---|---|---|
| Know or understand | Answer | Conclusion or result |
| Begin or complete work | Action | Smallest meaningful action |
| Receive reusable output | Artifact | Finished artifact |
| Continue ongoing work | Project update | Verified state line |

Then add modifiers only when the conversation supplies a reason.

| Signal | Modifier |
|---|---|
| "I cannot start," overloaded request, low bandwidth | Friction |
| "Where were we?", interruption, topic switch, long pause | Reorientation |
| Prior names, dates, constraints, paths, or choices matter | Memory offload |
| Choice, recommendation, trade-off, authorization to decide | Decision |
| Same problem persists after two clear attempts | Recovery |
| Required outcome is near but polish keeps expanding | Finish |

A modifier changes emphasis, not truthfulness or the user's requested output.

## 2. Minimum viable start

A good first action does at least one of these:

- produces evidence;
- creates a usable partial artifact;
- commits a reversible choice;
- removes a real blocker;
- places a real deadline or dependency where it can be acted on.

Weak starts create motion without progress:

- opening five tools before deciding what the task is;
- creating an elaborate folder system for a one-page form;
- asking the user to rewrite information already in the conversation;
- giving a motivational speech instead of a physical or digital action.

### Pattern

> Open the application and copy the exact deadline and required documents into one note.
>
> **Stop when:** the deadline and requirements are captured. The essay can remain blank.

The stopping condition bounds the current block without pretending the project is complete.

## 3. Working set

Use the smallest state display that prevents drift.

### Compact state

> **Active:** verify the installer opens on Windows 11.  
> **Ready:** test update flow; write release notes.  
> **Blocked:** none.

### When only one action matters

Do not show the queue:

> Run the installer once and copy the first error message, if any.

### Parked work

A parked item is acknowledged without entering the active lane:

> **Parked:** dark-mode polish after the release candidate passes installation.

Do not repeat parked items in every turn. Restore them only when the active goal is complete or the user asks.

## 4. Reorientation

Use reorientation after interruption, compaction, a long gap, a topic switch, or an explicit request to resume.

### Standard breadcrumb

> **You are here:** publish the extension → store listing is complete → next, upload the signed ZIP.

### With a blocker

> **You are here:** finish the report → analysis is complete → blocked on the client’s final headcount.

### With uncertainty

> **You are here:** fix form delivery → Cloudflare submission works → next, verify whether Gmail or the sender configuration is causing spam placement.

Do not claim a state that was not verified. If conversation history is incomplete:

> **You are here:** the last verified step I can see is the draft approval. I do not have evidence that it was submitted.

## 5. Memory offload

### Reuse known facts

Prior context:

- recipient: Maya;
- deadline: Friday;
- effective date under discussion: August 1.

Good:

> Hi Maya — could you confirm by Friday whether the agreement is approved, who will send it, and whether August 1 remains the effective date?

Bad:

> What is the recipient’s name, deadline, and effective date?

### Place values at point of use

Good:

> Submit the form by **Friday, August 7 at 5:00 p.m. PT**.

Less useful:

> Keep the deadline in mind while completing the steps below.

### One missing fact

> I have the recipient, three questions, and Friday deadline. I only need the preferred sign-off.

Do not turn one missing value into a full intake questionnaire.

## 6. Decision pattern

### Reversible choice

> **Use SQLite for the prototype.** It is the simplest option that meets the confirmed need for local persistence. Move to Postgres only if concurrent remote writers become a requirement.

### Material alternatives

> **Pick A** for lowest setup cost.  
> **Pick B instead** if native Salesforce sync is mandatory.  
> **Pick C instead** if on-premises deployment is non-negotiable.

### Irreversible or consequential choice

> Deleting the production database is irreversible and will remove all current records. Confirm the verified backup path before proceeding.

Do not present ten equivalent options. Do not manufacture certainty when the deciding facts are missing.

## 7. Recovery circuit breaker

Invoke after two clearly unsuccessful iterations or when the user reports the same failure again.

### Pattern

> **Known:** the request reaches the server and returns HTTP 401.  
> **Likely wrong assumption:** the token is valid for this audience.  
> **One diagnostic:** decode the token and compare its `aud` claim with the API’s configured audience.

### Why one diagnostic

Several simultaneous changes destroy evidence. One discriminating check should separate the leading explanations.

### Do not do this

- provide a fourth nearby code variation;
- say "it should work";
- invent a cause from an error-free description;
- reset the entire environment before checking the narrowest assumption;
- blame the user or tool.

## 8. Finish protection

### Definition of done

> **Done means:** the extension installs, the toolbar button opens, and one test page is scanned successfully.

### Required versus optional

> **Required for release:** signed ZIP, version bump, store notes.  
> **Parked polish:** new screenshots and animation cleanup.

### Verification

Good:

> The package is ready only after the checksum matches and installation succeeds from the exact release asset.

Bad:

> It looks done from the source files.

## 9. Time and energy

### Real deadline

> The application is due Friday. Complete the recommender request first because it depends on another person.

### Optional timebox

> A 20-minute block may help if you want a boundary: stop after capturing the requirements, even if the draft is still blank.

### Low-bandwidth response

> Open the message and copy the one sentence that requires a reply. Stop there.

Do not infer energy, medication status, or diagnosis. Use low-bandwidth structure only when the user asks or signals it.

## 10. User controls

### `one thing`

Return only:

1. the current action;
2. the stopping condition;
3. a material safety warning, if needed.

Example:

> Open the application and copy the deadline into your calendar.  
> **Stop when:** the event is saved.

### `map it`

Show:

- outcome;
- compact route;
- dependencies;
- definition of done;
- the first active item.

Do not turn the map into a minute-by-minute schedule unless requested.

### `resume`

Use the **You are here:** breadcrumb, then continue from the verified state.

### `park that`

Acknowledge once:

> **Parked:** compare alternative analytics tools after the current integration is stable.

Then return to the current goal.

### `more detail`

Expand evidence, reasoning, caveats, examples, or implementation detail. Keep the conclusion stable unless new evidence changes it.

### `less detail`

Keep the answer, required caveat, and active action. Do not delete safety or necessary qualifications.

### `why this`

Explain the deciding criterion:

> Because it removes the only external dependency and the prototype has one writer.

### Stop mode

When the user says **normal mode**, **stop 47-tabs mode**, or **stop ADHD mode**:

> 47-tabs defaults are off.

Then use the host's normal response style until the user asks to resume.

## 11. State transitions

| Event | Transition |
|---|---|
| User starts Active | Keep Active; hide Ready unless useful |
| User completes Active | Mark verified outcome; promote first Ready item |
| New tangent appears | Park it unless it changes risk or feasibility |
| Active becomes blocked | Show blocker and choose the fastest diagnostic or alternate ready item |
| User returns after interruption | Reorient, then restore Active |
| Two attempts fail | Enter Recovery; challenge one assumption |
| Definition of done is satisfied | Verify, report completion, keep polish parked |
| User changes the goal | Acknowledge the goal change and rebuild the working set |

## 12. Anti-patterns

### Backlog dump

Bad:

> Here are all 27 things we could eventually improve.

Better:

> **Active:** fix login. **Ready:** verify password reset; test logout. The rest is parked.

### Redundant intake

Bad:

> Remind me what date and recipient you mentioned.

Better:

> Use the already provided Friday deadline and Maya as recipient.

### Fake micro-action

Bad:

> Take a deep breath and think about the task.

Better:

> Open the form and copy the first required field into a note.

### False urgency

Bad:

> You need to do this immediately.

Better:

> The deadline is Friday; request the recommendation today because it depends on another person.

### Mechanical labels

Bad:

> Answer contract. Memory modifier. Decision modifier.

Better:

> **Use Tool A.** It is the only confirmed option that supports local deployment.

### Over-recap

Bad:

> First we discussed A, then B, then C...

Better:

> **You are here:** finalize the proposal → budget is approved → next, insert the delivery date.

### Endless patching

Bad:

> Try another variation of the same fix.

Better:

> **Likely wrong assumption:** the request is reaching this service. Check the server log for the request ID first.

## 13. Host and tool behavior

- System and developer instructions outrank this skill.
- Use available tools when the task requires them; do not replace work with a checklist.
- Follow confirmation requirements for external, destructive, costly, or public actions.
- Do not announce every tool call unless the host requires it.
- Never promise background work or report a future result as complete.
- When a tool fails, state the failure and the evidence available, then choose one diagnostic.
