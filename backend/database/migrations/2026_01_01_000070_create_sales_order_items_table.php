<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     * Tabel sales_order_items — detail baris per order penjualan
     */
    public function up(): void
    {
        Schema::create('sales_order_items', function (Blueprint $table) {
            $table->id();
            $table->foreignId('sales_order_id')
                  ->constrained('sales_orders')
                  ->cascadeOnDelete()
                  ->comment('Relasi ke header sales_orders');
            $table->foreignId('product_id')
                  ->constrained('products')
                  ->restrictOnDelete()
                  ->comment('Relasi ke tabel products');
            $table->integer('quantity')->comment('Jumlah item yang dipesan');
            $table->decimal('unit_price', 15, 2)->comment('Harga satuan saat order (snapshot harga)');
            $table->decimal('discount_percent', 5, 2)->default(0)->comment('Persentase diskon (0-100)');
            $table->decimal('tax_percent', 5, 2)->default(11)->comment('Persentase pajak PPN (default 11%)');

            // Kolom kalkulasi — di-generate dari aplikasi
            $table->decimal('subtotal', 15, 2)
                  ->storedAs('quantity * unit_price')
                  ->comment('Subtotal sebelum diskon dan pajak');
            $table->decimal('discount_amount', 15, 2)
                  ->storedAs('(quantity * unit_price) * (discount_percent / 100)')
                  ->comment('Nilai diskon dalam rupiah');
            $table->decimal('tax_amount', 15, 2)
                  ->storedAs('((quantity * unit_price) - ((quantity * unit_price) * (discount_percent / 100))) * (tax_percent / 100)')
                  ->comment('Nilai pajak PPN dalam rupiah');
            $table->decimal('total_price', 15, 2)
                  ->storedAs('((quantity * unit_price) - ((quantity * unit_price) * (discount_percent / 100))) * (1 + (tax_percent / 100))')
                  ->comment('Total harga akhir per baris item');

            $table->timestamps();

            // Index untuk join query performa
            $table->index('sales_order_id');
            $table->index('product_id');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('sales_order_items');
    }
};
