/* 3. FLECHITA DEL SIDEBAR – CORREGIDA */
[data-testid="stSidebarCollapsedControl"],
[data-testid="stExpandSidebarButton"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    position: fixed !important;
    top: 50% !important;
    left: 0 !important;
    transform: translateY(-50%) !important;
    z-index: 999999 !important;
    background-color: #161b22 !important;
    border: 1px solid #00ff87 !important;
    border-radius: 0 8px 8px 0 !important;
    padding: 10px 8px !important;
    cursor: pointer !important;
}

[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="stExpandSidebarButton"] svg,
[data-testid="collapsedControl"] svg,
[data-testid="stSidebarCollapseButton"] svg {
    fill: #00ff87 !important;
    color: #00ff87 !important;
    width: 22px !important;
    height: 22px !important;
    display: block !important;
    visibility: visible !important;
}
