from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Post, UserProfile, Comment, PageVisit, Newsletter
from django.contrib.auth.decorators import login_required


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def log_visit(request, path):
    if not request.session.session_key:
        request.session.save()
    PageVisit.objects.create(
        path=path,
        session_key=request.session.session_key,
        ip_address=get_client_ip(request),
        device_info=request.META.get('HTTP_USER_AGENT', '')[:255],
        referrer=request.META.get('HTTP_REFERER', '')[:255],
    )


@login_required
def home(request):
    log_visit(request, '/home/')
    posts = Post.objects.exclude(video='').exclude(video__isnull=True).order_by('-created_at')
    featured = posts.first()
    remaining_posts = posts.exclude(id=featured.id) if featured else posts
    return render(request, 'blog/home.html', {'posts': remaining_posts, 'featured': featured})

def blog_list(request, heading='Blog'):
    log_visit(request, '/blog/')
    posts = Post.objects.exclude(video='').exclude(video__isnull=True).order_by('-created_at')
    selected_category = request.GET.get('category')
    search_query = request.GET.get('search', '').strip()
    if selected_category:
        posts = posts.filter(category=selected_category)
    if search_query:
        posts = posts.filter(title__icontains=search_query)
    return render(request, 'blog/blog_list.html', {
        'posts': posts,
        'categories': Post.CATEGORY_CHOICES,
        'selected_category': selected_category,
        'page_heading': heading,
        'search_query': search_query,
    })

def photo_gallery(request):
    log_visit(request, '/photos/')
    posts = Post.objects.exclude(image='').exclude(image__isnull=True).order_by('-created_at')
    return render(request, 'blog/photo_gallery.html', {'posts': posts})

def all_comments(request):
    log_visit(request, '/comments/')
    comments = Comment.objects.all().order_by('-created_at')
    posts = Post.objects.all().order_by('-created_at')
    if request.method == 'POST':
        post_id = request.POST.get('post')
        text = request.POST.get('text')
        if post_id and text and request.user.is_authenticated:
            post = get_object_or_404(Post, id=post_id)
            Comment.objects.create(post=post, user=request.user, text=text)
            return redirect('all_comments')
    return render(request, 'blog/all_comments.html', {'comments': comments, 'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'GET':
        log_visit(request, f'/post/{post_id}/')
        post.views += 1
        post.save(update_fields=['views'])
    comments = post.comments.all().order_by('-created_at')
    if request.method == 'POST':
        text = request.POST.get('text')
        if text and request.user.is_authenticated:
            Comment.objects.create(post=post, user=request.user, text=text)
            return redirect('post_detail', post_id=post.id)
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = request.POST.get('email')
            user.save()
            gender = request.POST.get('gender')
            age = request.POST.get('age')
            place = request.POST.get('place')
            degree = request.POST.get('degree')
            course = request.POST.get('course')
            UserProfile.objects.create(user=user, gender=gender, age=age, place=place, degree=degree, course=course)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def add_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        video = request.FILES.get('video')
        image = request.FILES.get('image')
        category = request.POST.get('category', 'other')
        Post.objects.create(title=title, content=content, video=video, image=image, category=category)
        return redirect('home')
    return render(request, 'blog/add_post.html', {'categories': Post.CATEGORY_CHOICES})

def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        if request.FILES.get('video'):
            post.video = request.FILES.get('video')
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')
        post.save()
        return redirect('post_detail', post_id=post.id)
    return render(request, 'blog/edit_post.html', {'post': post})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'blog/delete_post.html', {'post': post})


@login_required
def analytics_dashboard(request):
    import json
    from django.db.models import Count
    from django.db.models.functions import TruncDate
    from urllib.parse import urlparse

    total_visits = PageVisit.objects.count()
    unique_visitors = PageVisit.objects.values('session_key').distinct().count()

    top_pages = (
        PageVisit.objects.values('path')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    daily_visits = (
        PageVisit.objects.annotate(day=TruncDate('visited_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    top_posts = Post.objects.order_by('-views')[:10]

    max_page_count = max([p['count'] for p in top_pages], default=1)
    max_post_views = max([p.views for p in top_posts], default=1)

    # New vs Returning: session with more than 1 visit = returning
    session_counts = PageVisit.objects.values('session_key').annotate(count=Count('id'))
    session_class = {}
    for s in session_counts:
        session_class[s['session_key']] = 'returning' if s['count'] > 1 else 'new'
    returning = sum(1 for v in session_class.values() if v == 'returning')
    new_visitors = unique_visitors - returning

    # Device breakdown + build detailed per-visit list for click-to-filter
    mobile_count = 0
    tablet_count = 0
    desktop_count = 0
    visit_details = []
    for v in PageVisit.objects.values('path', 'session_key', 'device_info', 'visited_at').order_by('-visited_at'):
        ua_lower = (v['device_info'] or '').lower()
        if 'tablet' in ua_lower or 'ipad' in ua_lower:
            device = 'Tablet'
            tablet_count += 1
        elif 'mobile' in ua_lower or 'android' in ua_lower or 'iphone' in ua_lower:
            device = 'Mobile'
            mobile_count += 1
        else:
            device = 'Desktop'
            desktop_count += 1
        visit_details.append({
            'path': v['path'],
            'device': device,
            'visitor_type': session_class.get(v['session_key'], 'new').capitalize(),
            'time': v['visited_at'].strftime('%b %d, %I:%M %p'),
        })

    # Top referrers
    referrer_counts = {}
    for ref in PageVisit.objects.exclude(referrer='').values_list('referrer', flat=True):
        try:
            domain = urlparse(ref).netloc or 'Direct'
        except Exception:
            domain = 'Other'
        referrer_counts[domain] = referrer_counts.get(domain, 0) + 1
    direct_count = PageVisit.objects.filter(referrer='').count()
    if direct_count:
        referrer_counts['Direct'] = referrer_counts.get('Direct', 0) + direct_count
    top_referrers = sorted(referrer_counts.items(), key=lambda x: -x[1])[:8]
    max_referrer_count = max([c for _, c in top_referrers], default=1)
    max_nr_count = max(new_visitors, returning, 1)
    max_device_count = max(desktop_count, mobile_count, tablet_count, 1)

    context = {
        'total_visits': total_visits,
        'unique_visitors': unique_visitors,
        'top_pages': top_pages,
        'daily_visits': list(daily_visits),
        'top_posts': top_posts,
        'max_page_count': max_page_count,
        'max_post_views': max_post_views,
        'new_visitors': new_visitors,
        'returning_visitors': returning,
        'mobile_count': mobile_count,
        'tablet_count': tablet_count,
        'desktop_count': desktop_count,
        'top_referrers': top_referrers,
        'max_referrer_count': max_referrer_count,
        'max_nr_count': max_nr_count,
        'max_device_count': max_device_count,
        'visit_details_json': json.dumps(visit_details),
    }
    return render(request, 'blog/analytics_dashboard.html', context)


def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            Newsletter.objects.get_or_create(email=email)
    return redirect('home')


@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_posts = Post.objects.filter().order_by('-created_at')
    user_comments = Comment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'blog/user_profile.html', {
        'profile': profile,
        'user_comments': user_comments,
    })