import { BarChart3, Moon, Settings, HelpCircle } from "lucide-react";

/**
 * Vertical rail of utility icon buttons on the right edge of the screen.
 * Purely presentational for now — wire up onClick handlers as real
 * features (e.g. usage stats, dark/light toggle, settings panel) are added.
 */
export default function IconRail() {
  const items = [
    { icon: BarChart3, label: "Usage stats" },
    { icon: Moon, label: "Toggle theme" },
    { icon: Settings, label: "Settings" },
  ];

  return (
    <div className="icon-rail">
      {items.map(({ icon: Icon, label }) => (
        <button key={label} className="icon-btn" title={label} aria-label={label}>
          <Icon size={18} strokeWidth={1.75} />
        </button>
      ))}
      <div className="icon-rail-spacer" />
      <button className="icon-btn icon-btn-help" title="Help" aria-label="Help">
        <HelpCircle size={18} strokeWidth={1.75} />
      </button>
    </div>
  );
}
