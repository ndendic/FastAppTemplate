from fasthtml.common import *
from monsterui.franken import *

def ModernCard(
    title=None,
    subtitle=None,
    content=None,
    footer=None,
    image_url=None,
    hover_effect=True,
    variant="default",  # default, primary, secondary, outline
    cls="",
):
    # Base card classes
    card_classes = [
        "rounded-xl border bg-card text-card-foreground shadow transition-all duration-300",
        "overflow-hidden",  # For image handling
    ]
    
    # Variant specific classes
    variant_classes = {
        "default": "",
        "primary": "border-primary/50 bg-primary/5",
        "secondary": "border-secondary/50 bg-secondary/5",
        "outline": "bg-transparent",
    }
    
    # Hover effect
    if hover_effect:
        card_classes.append("hover:shadow-lg hover:-translate-y-1")
    
    # Add variant classes
    card_classes.append(variant_classes.get(variant, ""))
    
    # Add custom classes
    if cls:
        card_classes.append(cls)

    return Div(cls=" ".join(card_classes))(
        # Image section
        Div(
            Img(
                src=image_url,
                alt=title if title else "Card image",
                cls="w-full h-48 object-cover",
            ),
            cls="w-full"
        ) if image_url else None,
        
        # Card body
        Div(cls="p-6 space-y-4")(
            # Header section
            Div(cls="space-y-1")(
                H3(title, cls="text-2xl font-semibold leading-none tracking-tight") if title else None,
                P(subtitle, cls="text-sm text-muted-foreground") if subtitle else None,
            ) if title or subtitle else None,
            
            # Content section
            Div(
                content,
                cls="text-sm text-muted-foreground"
            ) if content else None,
        ),
        
        # Footer section
        Div(
            footer,
            cls="p-6 pt-0"
        ) if footer else None,
    )

# Example usage:
def CardShowcase():
    return Container(
        H2("Modern Cards Showcase", cls="text-3xl font-bold mb-8"),
        
        # Grid of different card variants
        Grid(cols=2, gap=6)(
            # Default card with image
            ModernCard(
                title="Mountain Adventure",
                subtitle="Explore the peaks",
                content="Discover the breathtaking views from the highest mountains in the world.",
                image_url="https://images.unsplash.com/photo-1519681393784-d120267933ba",
                footer=Button("Learn More", variant="primary"),
            ),
            
            # Primary variant
            ModernCard(
                title="Technology",
                subtitle="Future is now",
                content="Explore the latest technological advancements shaping our world.",
                variant="primary",
                footer=DivRAligned(
                    Button("View Details", variant="primary"),
                    Button("Share", variant="outline"),
                    cls="space-x-2"
                ),
            ),
            
            # Secondary variant with no image
            ModernCard(
                title="Quick Tips",
                content="Learn how to improve your productivity with these simple steps.",
                variant="secondary",
                footer=Label("Productivity", cls=LabelT.secondary),
            ),
            
            # Outline variant
            ModernCard(
                title="Newsletter",
                subtitle="Stay updated",
                content="Subscribe to our newsletter to receive the latest updates.",
                variant="outline",
                footer=Input(placeholder="Enter your email", cls="w-full"),
            ),
        ),
    ) 