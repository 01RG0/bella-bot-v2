import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "./ui/dialog";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Switch } from "./ui/switch";
import { Loader2, Sparkles, Image as ImageIcon } from "lucide-react";
import { toast } from "sonner";

export function ImageGenerator() {
    const [model, setModel] = useState("flux");
    const [prompt, setPrompt] = useState("");
    const [width, setWidth] = useState(1024);
    const [height, setHeight] = useState(1024);
    const [enhance, setEnhance] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [generatedImage, setGeneratedImage] = useState<string | null>(null);
    const [availableModels, setAvailableModels] = useState<string[]>(["flux", "turbo", "stable-diffusion"]);

    // Fetch current model and available models on mount
    useEffect(() => {
        fetchModels();
    }, []);

    const fetchModels = async () => {
        try {
            const apiBase = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';
            const res = await fetch(`${apiBase}/api/image/models`);
            const data = await res.json();
            if (data.models) setAvailableModels(data.models);
            if (data.current_model) setModel(data.current_model);
        } catch (error) {
            console.error("Failed to fetch models", error);
        }
    };

    const handleGenerate = async () => {
        if (!prompt) return;
        setIsLoading(true);
        setGeneratedImage(null);
        try {
            const apiBase = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';
            const res = await fetch(`${apiBase}/api/image/generate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    prompt,
                    model,
                    width,
                    height,
                    enhance
                })
            });

            if (!res.ok) throw new Error("Generation failed");

            const data = await res.json();
            setGeneratedImage(data.image_url);
            toast.success("Image generated successfully!");
        } catch (error) {
            toast.error("Failed to generate image");
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSetDefaultModel = async (newModel: string) => {
        try {
            const apiBase = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';
            await fetch(`${apiBase}/api/image/model?model=${newModel}`, { method: 'POST' });
            // Update local state is handled by the model selection
            toast.success(`Default model set to ${newModel}`);
        } catch (error) {
            toast.error("Failed to set default model");
        }
    };

    return (
        <Dialog>
            <DialogTrigger asChild>
                <Button variant="outline" className="w-full justify-start gap-2">
                    <ImageIcon className="h-4 w-4" />
                    Image Generator
                </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[600px] max-h-[85vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle>AI Image Generator</DialogTitle>
                </DialogHeader>

                <div className="grid gap-4 py-4">
                    <div className="grid gap-2">
                        <Label>Prompt</Label>
                        <Input
                            placeholder="Describe your image..."
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                        />
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div className="grid gap-2">
                            <Label>Model</Label>
                            <Select value={model} onValueChange={(val: string) => { setModel(val); handleSetDefaultModel(val); }}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Select model" />
                                </SelectTrigger>
                                <SelectContent>
                                    {availableModels.map(m => (
                                        <SelectItem key={m} value={m}>{m}</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>

                        <div className="flex items-center space-x-2 pt-8">
                            <Switch id="enhance" checked={enhance} onCheckedChange={setEnhance} />
                            <Label htmlFor="enhance" className="flex items-center gap-1 cursor-pointer">
                                <Sparkles className="h-3 w-3" /> Enhance Prompt
                            </Label>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <div className="flex justify-between items-center">
                            <Label>Dimensions: <span className="text-muted-foreground">{width}x{height}</span></Label>
                        </div>
                        {/* Resolution Presets */}
                        <div className="flex flex-wrap gap-2">
                            <Button variant={width === 512 && height === 512 ? "secondary" : "outline"} size="sm" onClick={() => { setWidth(512); setHeight(512); }}>512x512</Button>
                            <Button variant={width === 1024 && height === 1024 ? "secondary" : "outline"} size="sm" onClick={() => { setWidth(1024); setHeight(1024); }}>1024x1024</Button>
                            <Button variant={width === 1920 && height === 1080 ? "secondary" : "outline"} size="sm" onClick={() => { setWidth(1920); setHeight(1080); }}>16:9</Button>
                            <Button variant={width === 1080 && height === 1920 ? "secondary" : "outline"} size="sm" onClick={() => { setWidth(1080); setHeight(1920); }}>9:16</Button>
                        </div>
                    </div>

                    <Button onClick={handleGenerate} disabled={isLoading || !prompt} className="w-full">
                        {isLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Sparkles className="mr-2 h-4 w-4" />}
                        Generate Image
                    </Button>

                    {generatedImage && (
                        <div className="mt-4 rounded-lg overflow-hidden border bg-black/5 flex items-center justify-center">
                            <a href={generatedImage} target="_blank" rel="noopener noreferrer">
                                <img src={generatedImage} alt="Generated" className="max-w-full max-h-[400px] object-contain hover:opacity-95 transition-opacity" />
                            </a>
                        </div>
                    )}
                </div>
            </DialogContent>
        </Dialog>
    );
}
