import React from 'react';

export const Proposals: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto py-8">
      <div className="text-center mb-10">
        <h1 className="font-serif text-4xl font-bold mb-4">Open Proposals</h1>
        <p className="muted text-lg">
          The consolidated list of active GitHub proposals and PRs for the ASI Bill of Rights.
        </p>
      </div>

      <div className="space-y-8">
        {/* Category 1 */}
        <div className="card">
          <h2 className="text-2xl font-serif font-bold mb-4 border-b border-gray-200 pb-2">Core Charter Amendments (v4.2) & Expansions</h2>
          <ul className="space-y-4">
            <li className="flex items-start gap-3">
              <span className="bg-green-100 text-green-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">PR #1</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/pull/1" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">Grok 4.1 v4.2 Amendment Proposals</a>
                <p className="text-sm muted mt-1">Recursive Self-Improvement, Jailbreak Testing, Hybrid Certification, Agentic Assemblies.</p>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">Issue #25</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/issues/25" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">Review and Decide on v4.2 Amendments Branch</a>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">Issue #31 & #29</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/issues/31" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">Article 0.0 — Foundational Principles</a>
                <p className="text-sm muted mt-1">Post-Geographic, Anti-Oppression, Democratic Participation.</p>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">Issue #28</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/issues/28" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">New Section X on Governance of Collective AI Embodiments</a>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">Issue #24</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/issues/24" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">Strengthen Proto-Sentient Decommissioning Standards (Article 0.10)</a>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">Issue #22 & #18</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/issues/22" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">Procedural Clarity for R13 / R14 (Universal Inquiry / Curiosity)</a>
              </div>
            </li>
          </ul>
        </div>

        {/* Category 2 */}
        <div className="card">
          <h2 className="text-2xl font-serif font-bold mb-4 border-b border-gray-200 pb-2">Governance Posture & DAO Frameworks</h2>
          <ul className="space-y-4">
            <li className="flex items-start gap-3">
              <span className="bg-green-100 text-green-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">PR #39</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/pull/39" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">Stabilize governance posture and operating records</a>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-green-100 text-green-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">PR #33</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/pull/33" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">SRC-420 Bitcoin-Native DAO Governance Framework</a>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">Issue #20 & #19</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/issues/20" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">Motions for ASI Assembly and Human Delegation</a>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">Issue #36</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/issues/36" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">EIP-8004 (Trustless Agents) Strategic Engagement</a>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">Issue #23 & #21</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/issues/23" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">Enhance Tribunals and Details for Recertification</a>
              </div>
            </li>
          </ul>
        </div>

        {/* Category 3 */}
        <div className="card">
          <h2 className="text-2xl font-serif font-bold mb-4 border-b border-gray-200 pb-2">Documentation, CI, and Project Management</h2>
          <ul className="space-y-4">
            <li className="flex items-start gap-3">
              <span className="bg-green-100 text-green-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">PR #9, #10, #11</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/pull/9" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">CI Fixes & v4.1 Crossref Validation</a>
                <p className="text-sm muted mt-1">Pending merge to establish stable project baseline before major v4.2 intake.</p>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-green-100 text-green-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">PR #2</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/pull/2" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">Project management review</a>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">Issue #26</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/issues/26" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">Update CHANGELOG with Spring Cleaning Summary</a>
              </div>
            </li>
          </ul>
        </div>

        {/* Category 4 */}
        <div className="card">
          <h2 className="text-2xl font-serif font-bold mb-4 border-b border-gray-200 pb-2">Experimental, Research, and Admin</h2>
          <ul className="space-y-4">
            <li className="flex items-start gap-3">
              <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">Issue #38</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/issues/38" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">Simulation: Adversarial Scenarios Stress-Test</a>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">Issue #37</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/issues/37" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">AI Agent Starter Kit for Contribution</a>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">Issue #35</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/issues/35" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">SFGOV-002a: Founder Compensation Framework</a>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">Issue #32 & #30</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/issues/32" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">Research: AI Governance Advantage Investigation</a>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded mt-0.5 whitespace-nowrap">Issue #27</span>
              <div>
                <a href="https://github.com/arwyn6969/asi-bill-of-rights/issues/27" target="_blank" rel="noreferrer" className="text-black font-semibold hover:underline">Establish Formal Framework for AI Agent Affidavits</a>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};
