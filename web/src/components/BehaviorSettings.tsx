import { useState, useEffect } from 'react';
import { Button } from "./ui/button";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "./ui/dialog";
import { Label } from "./ui/label";
import { Textarea } from "./ui/textarea";
import { Input } from "./ui/input";
import { BrainCircuit, Trash2, Plus } from 'lucide-react';
import { toast } from 'sonner';

// @ts-ignore
const API_BASE = (import.meta as any).env.VITE_API_BASE_URL ?? 'http://localhost:8000';

export function BehaviorSettings() {
    const [config, setConfig] = useState<any>(null);
    const [activeTab, setActiveTab] = useState('personas');
    const [newPersonaName, setNewPersonaName] = useState('');

    const fetchConfig = async () => {
        try {
            const res = await fetch(`${API_BASE}/api/behaviors/config`);
            const data = await res.json();
            setConfig(data);
        } catch (e) {
            console.error(e);
            toast.error("Failed to load behavior config");
        }
    };

    useEffect(() => {
        fetchConfig();
    }, []);

    const savePersona = async (id: string, name: string, prompt: string) => {
        // Optimistic update
        const next = { ...config };
        next.personas[id] = { name, prompt };
        setConfig(next);

        try {
            const res = await fetch(`${API_BASE}/api/behaviors/persona`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id, name, prompt }),
            });
            if (res.ok) {
                toast.success("Saved");
            }
        } catch (e) {
            toast.error("Error saving");
            fetchConfig(); // Revert
        }
    };

    const createPersona = async () => {
        if (!newPersonaName) return;
        const id = `p_${Date.now()}`;
        await savePersona(id, newPersonaName, "");
        setNewPersonaName("");
        toast.success("Created persona " + newPersonaName);
    };

    const deletePersona = async (id: string) => {
        if (!confirm("Delete this persona?")) return;
        try {
            await fetch(`${API_BASE}/api/behaviors/persona/${id}`, { method: 'DELETE' });
            fetchConfig();
            toast.success("Deleted");
        } catch { toast.error("Error deleting"); }
    };

    const saveGuidelines = async (text: string) => {
        await fetch(`${API_BASE}/api/behaviors/guidelines`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text }),
        });
        fetchConfig();
        toast.success("Guidelines Saved");
    };

    const assign = async (type: 'user' | 'role', target: string, personaId: string) => {
        await fetch(`${API_BASE}/api/behaviors/assign/${type}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userId: target, role: target, personaId }),
        });
        fetchConfig();
        toast.success("Assigned");
    };

    if (!config) return null;

    return (
        <Dialog>
            <DialogTrigger asChild>
                <Button variant="outline" className="w-full justify-start gap-2">
                    <BrainCircuit className="h-4 w-4" />
                    AI Personality Controller
                </Button>
            </DialogTrigger>
            <DialogContent className="max-w-4xl h-[80vh] flex flex-col p-6">
                <DialogHeader>
                    <DialogTitle>Behavior & Personality Control</DialogTitle>
                </DialogHeader>

                <div className="flex gap-4 mb-4 border-b">
                    <Button variant={activeTab === 'personas' ? 'default' : 'ghost'} onClick={() => setActiveTab('personas')}>Personas</Button>
                    <Button variant={activeTab === 'assignments' ? 'default' : 'ghost'} onClick={() => setActiveTab('assignments')}>Assignments</Button>
                    <Button variant={activeTab === 'global' ? 'default' : 'ghost'} onClick={() => setActiveTab('global')}>Global Rules</Button>
                </div>

                <div className="flex-1 overflow-y-auto pr-2">
                    {activeTab === 'personas' && (
                        <div className="space-y-6">
                            <div className="flex gap-2 items-end p-4 bg-neutral-50 rounded-lg">
                                <div className="flex-1">
                                    <Label>New Persona Name</Label>
                                    <Input value={newPersonaName} onChange={e => setNewPersonaName(e.target.value)} placeholder="e.g. Angry Bella" />
                                </div>
                                <Button onClick={createPersona}><Plus className="w-4 h-4 mr-2" /> Create</Button>
                            </div>

                            {Object.entries(config.personas).map(([id, p]: any) => (
                                <div key={id} className="border rounded-lg p-4 space-y-3">
                                    <div className="flex justify-between items-center bg-neutral-100 p-2 rounded">
                                        <Input className="max-w-[200px] font-bold border-none bg-transparent" value={p.name} onChange={(e) => savePersona(id, e.target.value, p.prompt)} />
                                        <div className="flex items-center gap-2">
                                            <span className="text-xs text-neutral-400 font-mono">{id}</span>
                                            <Button variant="ghost" size="icon" className="text-red-500 hover:text-red-700 hover:bg-red-50" onClick={() => deletePersona(id)}><Trash2 className="w-4 h-4" /></Button>
                                        </div>
                                    </div>
                                    <Textarea
                                        className="min-h-[100px]"
                                        value={p.prompt}
                                        onChange={(e) => {
                                            const next = { ...config };
                                            next.personas[id].prompt = e.target.value;
                                            setConfig(next);
                                        }}
                                        onBlur={() => savePersona(id, p.name, p.prompt)}
                                        placeholder="System Prompt..."
                                    />
                                </div>
                            ))}
                        </div>
                    )}

                    {activeTab === 'assignments' && (
                        <div className="space-y-6">
                            <div className="p-4 border rounded-lg">
                                <h3 className="font-semibold mb-4">Role Assignments</h3>
                                {config.assignments.roles && Object.entries(config.assignments.roles).map(([role, pid]: any) => (
                                    <div key={role} className="flex items-center gap-2 mb-2 p-2 bg-neutral-50 rounded">
                                        <span className="w-32 font-mono font-bold text-blue-600">{role}</span>
                                        <span className="text-neutral-400">→</span>
                                        <span className="font-bold">{config.personas[pid]?.name || pid}</span>
                                        <Button variant="ghost" size="sm" onClick={() => assign('role', role, "")}><Trash2 className="w-4 h-4" /></Button>
                                    </div>
                                ))}
                                <div className="flex gap-2 mt-4 items-end">
                                    <div>
                                        <Label className="text-xs">Role Name</Label>
                                        <Input id="newRole" placeholder="e.g. Admin" />
                                    </div>
                                    <div className="flex-1">
                                        <Label className="text-xs">Assign Persona</Label>
                                        <select id="rolePersona" className="w-full h-10 border rounded px-3 bg-white">
                                            {Object.entries(config.personas).map(([id, p]: any) => (
                                                <option key={id} value={id}>{p.name}</option>
                                            ))}
                                        </select>
                                    </div>
                                    <Button onClick={() => {
                                        const role = (document.getElementById('newRole') as HTMLInputElement).value;
                                        const pid = (document.getElementById('rolePersona') as HTMLSelectElement).value;
                                        if (role) assign('role', role, pid);
                                    }}>Assign Role</Button>
                                </div>
                            </div>

                            <div className="p-4 border rounded-lg mt-4">
                                <h3 className="font-semibold mb-4">User Assignments (Overrides)</h3>
                                {config.assignments.users && Object.entries(config.assignments.users).map(([uid, pid]: any) => (
                                    <div key={uid} className="flex items-center gap-2 mb-2 p-2 bg-neutral-50 rounded">
                                        <span className="w-32 font-mono text-xs text-neutral-500 overflow-hidden">{uid}</span>
                                        <span className="text-neutral-400">→</span>
                                        <span className="font-bold">{config.personas[pid]?.name || pid}</span>
                                        <Button variant="ghost" size="sm" onClick={() => assign('user', uid, "")}><Trash2 className="w-4 h-4" /></Button>
                                    </div>
                                ))}
                                <div className="flex gap-2 mt-4 items-end">
                                    <div>
                                        <Label className="text-xs">User ID</Label>
                                        <Input id="newUser" placeholder="Discord User ID" />
                                    </div>
                                    <div className="flex-1">
                                        <Label className="text-xs">Assign Persona</Label>
                                        <select id="userPersona" className="w-full h-10 border rounded px-3 bg-white">
                                            {Object.entries(config.personas).map(([id, p]: any) => (
                                                <option key={id} value={id}>{p.name}</option>
                                            ))}
                                        </select>
                                    </div>
                                    <Button onClick={() => {
                                        const uid = (document.getElementById('newUser') as HTMLInputElement).value;
                                        const pid = (document.getElementById('userPersona') as HTMLSelectElement).value;
                                        if (uid) assign('user', uid, pid);
                                    }}>Assign User</Button>
                                </div>
                            </div>
                        </div>
                    )}

                    {activeTab === 'global' && (
                        <div className="space-y-4">
                            <Label>Global Guidelines (Appended to ALL personas)</Label>
                            <p className="text-sm text-neutral-500">Use this for rules that apply to everyone, like "Savage Mode" triggers or basic identity.</p>
                            <Textarea
                                className="min-h-[300px] font-mono text-sm"
                                value={config.global_guidelines}
                                onChange={(e) => setConfig({ ...config, global_guidelines: e.target.value })}
                            />
                            <Button onClick={() => saveGuidelines(config.global_guidelines)}>Save Guidelines</Button>
                        </div>
                    )}
                </div>
            </DialogContent>
        </Dialog>
    );
}
